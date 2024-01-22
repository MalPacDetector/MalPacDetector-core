import os
import shutil
import argparse
import traceback
import json
import tarfile

from training import (
    PreprocessMethodEnum,
    ModelEnum,
    ActionEnum,
    train,
    predict_package_MLP,
    predict_package_NB,
    predict_package_SVM,
    predict_package_RF
)
from conf import SETTINGS


def load_settings():
    """Load settings.

    Returns:
        Settings.
    """
    settings_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf/settings.json')
    try:
        with open(settings_file_path, 'r') as f:
            current_settings = json.load(f)
    except FileNotFoundError:
        print(f'Error: {settings_file_path} not found!')
        exit(1)
    except json.decoder.JSONDecodeError:
        print(f'Error: {settings_file_path} is not a valid json file!')
        exit(1)
    return current_settings

def add_mode(dir: str):
    """
    Check if the folder has read, write and execute permissions, if not, add them.
    Check if the file has read and write permissions, if not, add them.

    Args:
        dir: Folder path.
    """
    if not os.path.exists(dir):
        return
    for dirpath, dirnames, filenames in os.walk(dir):
        for dirname in dirnames:
            dir_path = os.path.join(dirpath, dirname)
            if not os.access(dir_path, os.R_OK | os.W_OK | os.X_OK):
                os.chmod(dir_path, 0o777)
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if not os.access(file_path, os.R_OK | os.W_OK):
                os.chmod(file_path, 0o666)

def decompress_packages(dataset_path: str, use_cache: bool = False) -> str:
    """Decompress packages.
    
    Args:
        dataset_path: Path of dataset.
        use_cache: Use cache or not.

    Returns:
        Path of decompressed dataset.
    """
    temp_base_path = os.path.abspath(f'.decompressed-packages')
    temp_dataset_path = os.path.abspath(os.path.join(temp_base_path, os.path.basename(dataset_path)))

    if use_cache and os.path.exists(temp_dataset_path):
        return temp_dataset_path
    if os.path.exists(temp_dataset_path):
        try:
            shutil.rmtree(temp_dataset_path)
        except PermissionError:
            print(f'Error: Delete temp dataset folder {temp_dataset_path} failed.')
            traceback.print_exc()
            add_mode(temp_dataset_path)
            shutil.rmtree(temp_dataset_path)
    os.makedirs(temp_dataset_path)
    dataset_names = os.listdir(dataset_path)
    for counter, file_name in enumerate(dataset_names):
        print(f'{counter + 1}/{len(dataset_names)}: Decompressing {file_name}...')
        file_path = os.path.join(dataset_path, file_name)
        try:
            # decompress .tar.gz file
            if file_name.endswith('.tar.gz'):
                tar = tarfile.open(file_path)
                temp_package_path = f'{temp_dataset_path}/{file_name[:-7]}'
                os.makedirs(temp_package_path, exist_ok=True)
                tar.extractall(path=temp_package_path)
                tar.close()
            # decompress .tgz file
            elif file_name.endswith('.tgz'):
                tar = tarfile.open(file_path)
                temp_package_path = f'{temp_dataset_path}/{file_name[:-4]}'
                os.makedirs(temp_package_path, exist_ok=True)
                tar.extractall(path=temp_package_path)
                tar.close()
        except Exception:
            print(f'Error: Decompress the package {file_name} failed.')
            traceback.print_exc()
    add_mode(temp_dataset_path)
    return temp_dataset_path

def extract_cli():
    """Extract features from given dataset."""
    dataset_names = args.dataset
    use_cache = args.cache
    for dataset_name in dataset_names:
        dataset_path = os.path.join(SETTINGS['path']['datasets'], dataset_name)
        dataset_path = os.path.abspath(decompress_packages(dataset_path, use_cache))
        if not os.path.exists(dataset_path):
            print(f'Error: Dataset path {dataset_path} not found!')
            exit(1)
        feature_path = os.path.abspath(os.path.join(SETTINGS['path']['features'], dataset_name))
        feature_position_path = os.path.abspath(os.path.join(SETTINGS['path']['feature-positions'], dataset_name))

        if os.path.exists(feature_path):
            try:
                shutil.rmtree(feature_path)
            except PermissionError:
                print(f'Error: Delete feature folder {feature_path} failed.')
                traceback.print_exc()
        os.makedirs(feature_path)

        if os.path.exists(feature_position_path):
            try:
                shutil.rmtree(feature_position_path)
            except PermissionError:
                print(f'Error: Delete feature position folder {feature_path} failed.')
                traceback.print_exc()
        os.makedirs(feature_position_path)

        try:
            cwd = os.getcwd()
            os.chdir('feature-extract')
            os.system(f'npm run start -- -d {dataset_path} {feature_path} {feature_position_path}')
            os.chdir(cwd)
        except Exception:
            print(f'Error: Extract feature of dataset {dataset_name} failed.')
            traceback.print_exc()

def train_cli():
    """Train model with given dataset."""
    malicious_dataset_names = args.malicious
    benign_dataset_names = args.benign
    model_name = args.model
    preprocess_method = args.preprocess
    action_name = args.action
    malicous_csv_dir_paths = []
    benign_csv_dir_paths = []
    for malicious_dataset_name in malicious_dataset_names:
        malicous_csv_dir_paths.append(os.path.join(SETTINGS['path']['features'], malicious_dataset_name))
    for benign_dataset_name in benign_dataset_names:
        benign_csv_dir_paths.append(os.path.join(SETTINGS['path']['features'], benign_dataset_name))
    hyperparameters = {}

    if preprocess_method == 'none':
        preprocess = PreprocessMethodEnum.NONE
    elif preprocess_method == 'standardlize':
        preprocess = PreprocessMethodEnum.STANDARDLIZE
    elif preprocess_method == 'min-max-scale':
        preprocess = PreprocessMethodEnum.MIN_MAX_SCALE

    if action_name == 'training':
        action = ActionEnum.TRAINING
    elif action_name == 'save':
        action = ActionEnum.SAVE

        if model_name == 'MLP':
            hyperparameters['learning_rate'] = args.hyper_rate
            hyperparameters['number_of_hidden_units'] = args.hyper_layers
            hyperparameters['number_of_iterations'] = args.hyper_iterations
            hyperparameters['optimization'] = args.hyper_optimization
            hyperparameters['activation'] = args.hyper_activation
        elif model_name == 'NB':
            hyperparameters['smoothing'] = args.hyper_smoothing
        elif model_name == 'SVM':
            try:
                hyperparameters['gamma'] = float(args.hyper_gamma)
            except Exception:
                hyperparameters['gamma'] = args.hyper_gamma
            hyperparameters['C'] = args.hyper_C
        elif model_name == 'RF':
            hyperparameters['number_of_decision_trees'] = args.hyper_trees
            hyperparameters['maxium_depth'] = args.hyper_depth
    
    if model_name == 'MLP':
        model = ModelEnum.MLP
    elif model_name == 'NB':
        model = ModelEnum.NB
    elif model_name == 'SVM':
        model = ModelEnum.SVM
    elif model_name == 'RF':
        model = ModelEnum.RF

    train(malicous_csv_dir_paths, benign_csv_dir_paths, preprocess, model, action, hyperparameters)

def predict_cli():
    """Predict packages."""
    dataset_names = args.dataset
    model_name = args.model

    for dataset_name in dataset_names:
        report_name = f'{dataset_name}-{model_name}-report.csv'
        report_content = 'package name, predict\n'
        csv_dir_path = os.path.join(SETTINGS['path']['features'], dataset_name)
        for feature_file_name in os.listdir(csv_dir_path):
            feature_file_path = os.path.join(csv_dir_path, feature_file_name)
            if model_name == 'MLP':
                result = predict_package_MLP(feature_file_path)
            elif model_name == 'NB':
                result = predict_package_NB(feature_file_path)
            elif model_name == 'SVM':
                result = predict_package_SVM(feature_file_path)
            elif model_name == 'RF':
                result = predict_package_RF(feature_file_path)
            report_content += feature_file_name[:-4] + ', ' + result + '\n'

        with open(os.path.join(SETTINGS['path']['reports'], report_name), 'w') as f:
            f.write(report_content)

def predict_single_package(package_path: str):
    """Extract features and predict from given path."""
    package_path = args.package_path
    package_name = os.path.basename(package_path)
    if not os.path.exists(package_path):
        print(f'Error: Package path {package_path} not found!')
        exit(1)
    feature_path = os.path.abspath(SETTINGS['path']['features'])
    feature_position_path = os.path.abspath(SETTINGS['path']['feature-positions'])

    try:
        cwd = os.getcwd()
        os.chdir('feature-extract')
        os.system(f'npm run start -- -p {package_path} {feature_path} {feature_position_path}')
        os.chdir(cwd)
    except Exception:
        print(f'Error: Extract feature of package {package_path} failed.')
        traceback.print_exc()

    model_name = args.model
    feature_positions_file_path = os.path.join(SETTINGS['path']['feature-positions'], f'{package_name}.json')
    if not os.path.exists(feature_positions_file_path):
        print(f'Error: Feature positions file {feature_positions_file_path} not found!')
        exit(1)
    with open(feature_positions_file_path, 'r') as f:
        feature_positions = json.load(f)

    report_name = f'{package_name}-{model_name}.json'
    report_dir_path = os.path.join(SETTINGS['path']['features'])
    feature_file_path = os.path.join(report_dir_path, f'{package_name}.csv')
    if model_name == 'MLP':
        result = predict_package_MLP(feature_file_path)
    elif model_name == 'NB':
        result = predict_package_NB(feature_file_path)
    elif model_name == 'SVM':
        result = predict_package_SVM(feature_file_path)
    elif model_name == 'RF':
        result = predict_package_RF(feature_file_path)
    report_content = json.dumps({
        'prediction': result,
        'feature_positions': feature_positions
    })

    with open(os.path.join(SETTINGS['path']['reports'], report_name), 'w') as f:
        f.write(report_content)

if __name__ == '__main__':
    settings = load_settings()
    DATASET_NAMES = [f for f in os.listdir(settings['path']['datasets']) if os.path.isdir(os.path.join(settings['path']['datasets'], f))]
    FEATURE_NAMES = [f for f in os.listdir(settings['path']['features']) if os.path.isdir(os.path.join(settings['path']['features'], f))]
    MODEL_NAMES = settings['classifier']['models']
    PREPROCESS_METHOD_NAMES = settings['classifier']['preprocess_methods']

    hyperparameters = {}
    parser = argparse.ArgumentParser(description='Extract, train, and predict packages.')
    subparsers = parser.add_subparsers(help='sub-command help', dest='subparser_name')

    # extract CLI parameters
    parser_extract = subparsers.add_parser('extract', help='extract features', description='Extract features from given dataset.')
    parser_extract.add_argument('-d', '--dataset', type=str, required=True, help='dataset name', choices=DATASET_NAMES, nargs='+')
    parser_extract.add_argument('-c', '--cache', type=bool, help='use cache or not', default=False)

    # train CLI parameters
    parser_train = subparsers.add_parser('train', help='train model', description='Train model with given dataset.')
    parser_train.add_argument('-m', '--malicious', type=str, required=True, help='malicious dataset name', choices=FEATURE_NAMES, nargs='+')
    parser_train.add_argument('-b', '--benign', type=str, required=True, help='benign dataset name', choices=FEATURE_NAMES, nargs='+')
    parser_train.add_argument('-o', '--model', type=str, required=True, help='model name', choices=MODEL_NAMES)
    parser_train.add_argument('-p', '--preprocess', type=str, required=True, help='preprocess method', choices=PREPROCESS_METHOD_NAMES)
    parser_train.add_argument('-a', '--action', type=str, required=True, help='action', choices=['training', 'save'])

    # NB
    parser_train.add_argument('-hs', '--hyper-smoothing', type=float, help='smoothing of NB', choices=settings['classifier']['hyperparameters']['NB']['smoothings'])

    # MLP
    parser_train.add_argument('-hr', '--hyper-rate', type=float, help='learning rate of MLP', choices=settings['classifier']['hyperparameters']['MLP']['learning_rates'])
    parser_train.add_argument('-hl', '--hyper-layers', type=int, help='number of layers of MLP', choices=settings['classifier']['hyperparameters']['MLP']['number_of_hidden_units'])
    parser_train.add_argument('-hi', '--hyper-iterations', type=int, help='number of iterations of MLP', choices=settings['classifier']['hyperparameters']['MLP']['number_of_iterations'])
    parser_train.add_argument('-ho', '--hyper-optimization', type=str, help='optimization algorithm of MLP', choices=settings['classifier']['hyperparameters']['MLP']['optimization_algorithms'])
    parser_train.add_argument('-ha', '--hyper-activation', type=str, help='activation function of MLP', choices=settings['classifier']['hyperparameters']['MLP']['activation_functions'])

    # RF
    parser_train.add_argument('-he', '--hyper-trees', type=int, help='number of decision trees of RF', choices=settings['classifier']['hyperparameters']['RF']['number_of_decision_trees'])
    parser_train.add_argument('-hd', '--hyper-depth', type=int, help='maxium depth of RF', choices=settings['classifier']['hyperparameters']['RF']['maxium_depths'])

    # SVM
    parser_train.add_argument('-hg', '--hyper-gamma', type=str, help='gamma of SVM', choices=settings['classifier']['hyperparameters']['SVM']['gammas'])
    parser_train.add_argument('-hc', '--hyper-C', type=float, help='C of SVM', choices=settings['classifier']['hyperparameters']['SVM']['C'])

    # predict CLI parameters
    parser_predict = subparsers.add_parser('predict', help='predict package', description='Predict package with given model.')
    parser_predict.add_argument('-o', '--model', type=str, required=True, help='model name', choices=MODEL_NAMES)
    parser_predict.add_argument('-d', '--dataset', type=str, help='dataset name', choices=FEATURE_NAMES, nargs='+')
    parser_predict.add_argument('-p', '--package-path', type=str, help='absolute package path')

    args = parser.parse_args()

    subparser_name = args.subparser_name
    if subparser_name == 'extract':
        extract_cli()
    elif subparser_name == 'train':
        train_cli()
    elif subparser_name == 'predict':
        if args.package_path:
            predict_single_package(args.package_path)
        elif args.model:
            predict_cli()
        else:
            print('Error: Please specify package path or model name!')
            exit(1)
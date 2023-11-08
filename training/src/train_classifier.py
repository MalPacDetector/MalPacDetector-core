from enum import Enum

from sklearn.preprocessing import StandardScaler, MinMaxScaler

from .read_feature import read_features
from .train_MLP import train_MLP_validation, save_MLP
from .train_NB import train_NB_Validate, save_NB
from .train_RF import train_classifier_RF_Validation, save_RF
from .train_SVM import train_SVM_validate, save_SVM
from .pickle_util import save_scaler
from .commons import rf_scaler_save_path, mlp_scaler_save_path, nb_scaler_save_path, svm_scaler_save_path


class PreprocessMethodEnum(Enum):
    """Enumeration of data preprocessing methods."""
    NONE = 1
    STANDARDLIZE = 2
    MIN_MAX_SCALE = 3

class ModelEnum(Enum):
    """Enumeration of models."""
    RF = 1
    MLP = 2
    NB = 3
    SVM = 4

class ActionEnum(Enum):
    """Enumeration of actions."""
    TRAINING = 1
    SAVE = 2

def train(malcious_features_dir_path: str, normal_features_dir_path: str, preprocess_method: PreprocessMethodEnum, model: ModelEnum, action: ActionEnum, hyperparameters={}):
    """Train the model.
    
    Args:
        malcious_features_dir_path: The path of the directory containing multiple malicious sample feature files.
        normal_features_dir_path: The path of the directory containing multiple benign sample feature files.
        preprocess_method: The method of data preprocessing.
        model: The model to be trained.
        action: The action to be performed.
        hyperparameters: The hyperparameters of the model.
    """
    [X, y, _] = read_features(malcious_features_dir_path, normal_features_dir_path)
    X_train = X
    y_train = y

    # preprocess
    if model == ModelEnum.RF:
        scaler_save_path = rf_scaler_save_path
    elif model == ModelEnum.MLP:
        scaler_save_path = mlp_scaler_save_path
    elif model == ModelEnum.NB:
        scaler_save_path = nb_scaler_save_path
    elif model == ModelEnum.SVM:
        scaler_save_path = svm_scaler_save_path
    [X_train] = preprocess(X_train, scaler_save_path, preprocess_method)

    # training and validation
    if action == ActionEnum.TRAINING:
        if model == ModelEnum.RF:
            train_classifier_RF_Validation(X_train, y_train)
        elif model == ModelEnum.MLP:
            train_MLP_validation(X_train, y_train)
        elif model == ModelEnum.NB:
            train_NB_Validate(X_train, y_train)
        elif model == ModelEnum.SVM:
            train_SVM_validate(X_train, y_train)

    # save model
    elif action == ActionEnum.SAVE:
        if model == ModelEnum.RF:
            if hyperparameters.get('number_of_decision_trees') is None or hyperparameters.get('maxium_depth') is None:
                raise Exception('Hyperpameters cannot be empty.')
            save_RF(X_train, y_train, number_of_decision_trees=hyperparameters.get('number_of_decision_trees'), maxium_depth=hyperparameters.get('maxium_depth'))
        elif model == ModelEnum.MLP:
            if hyperparameters.get('learning_rate') is None or \
                hyperparameters.get('number_of_hidden_units') is None or \
                hyperparameters.get('number_of_iterations') is None or \
                hyperparameters.get('optimization') is None or \
                hyperparameters.get('activation') is None:
                raise Exception('Hyperpameters cannot be empty.')
            save_MLP(X_train, y_train, learning_rate=hyperparameters.get('learning_rate'), number_of_hidden_units=hyperparameters.get('number_of_hidden_units'), number_of_iterations=hyperparameters.get('number_of_iterations'), optimization=hyperparameters.get('optimization'), activation=hyperparameters.get('activation'))
        elif model == ModelEnum.NB:
            if hyperparameters.get('smoothing') is None:
                raise Exception('Hyperpameters cannot be empty.')
            save_NB(X_train, y_train, smoothing=hyperparameters.get('smoothing'))
        elif model == ModelEnum.SVM:
            if hyperparameters.get('gamma') is None or \
                hyperparameters.get('C') is None:
                raise Exception('Hyperpameters cannot be empty.')
            save_SVM(X_train, y_train, gamma=hyperparameters.get('gamma'), C=hyperparameters.get('C'))

def preprocess(X_train, scaler_save_path: str, preprocess_method: PreprocessMethodEnum) -> list:
    """Preprocess the data.
    
    Args:
        X_train: The training data.
        scaler_save_path: The path to save the scaler.
        preprocess_method: The method of data preprocessing.

    Returns:
        The preprocessed data.
    """
    if preprocess_method == PreprocessMethodEnum.NONE:
        return [X_train]
    if preprocess_method == PreprocessMethodEnum.STANDARDLIZE:
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train_scaled = scaler.transform(X_train)
        save_scaler(scaler, scaler_save_path)
        return [X_train_scaled]
    if preprocess_method == PreprocessMethodEnum.MIN_MAX_SCALE:
        scaler = MinMaxScaler()
        scaler.fit(X_train)
        X_train_scaled = scaler.transform(X_train)
        save_scaler(scaler, scaler_save_path)
        return [X_train_scaled]
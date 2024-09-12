from .pickle_util import load_classifier, load_scaler
from .read_feature import read_feature_from_file
from .commons import MLP_path, rf_scaler_save_path, mlp_scaler_save_path, nb_path,nb_scaler_save_path, svm_scaler_save_path,svm_path, rf_classifier_path


def predict_single_package(classifier, feature_vector):
    """Predict the label of a single package.
   
    Args:
         classifier: The classifier.
         feature_vector: The feature vector of the package.

    Returns:
        The predicted label of the package.
    """
    return classifier.predict(feature_vector)

def predict_package_MLP(feature_file_path):
    """Predict the label of a single package using MLP.
    
    Args:
        feature_file_path: The path of the feature file of the package.

    Returns:
        The predicted label of the package.
    """
    classifier = load_classifier(MLP_path)
    feature_vector = read_feature_from_file(feature_file_path)
    scaler_path = mlp_scaler_save_path
    scaler = load_scaler(scaler_path)
    feature_vector = scaler.transform([feature_vector])
    return predict_single_package(classifier, feature_vector)[0]

def predict_package_NB(feature_file_path):
    """Predict the label of a single package using NB.
    
    Args:
        feature_file_path: The path of the feature file of the package.

    Returns:
        The predicted label of the package.
    """
    classifier = load_classifier(nb_path)
    feature_vector = read_feature_from_file(feature_file_path)
    scaler_path = nb_scaler_save_path
    scaler = load_scaler(scaler_path)
    feature_vector = scaler.transform([feature_vector])
    return predict_single_package(classifier, feature_vector)[0]

def predict_package_SVM(feature_file_path):
    """Predict the label of a single package using SVM.
    
    Args:
        feature_file_path: The path of the feature file of the package.

    Returns:
        The predicted label of the package.
    """
    classifier = load_classifier(svm_path)
    feature_vector = read_feature_from_file(feature_file_path)
    scaler_path = svm_scaler_save_path
    scaler = load_scaler(scaler_path)
    feature_vector = scaler.transform([feature_vector])
    return predict_single_package(classifier, feature_vector)[0]

def predict_package_RF(feature_file_path):
    """Predict the label of a single package using RF.
    
    Args:
        feature_file_path: The path of the feature file of the package.

    Returns:
        The predicted label of the package.
    """
    classifier = load_classifier(rf_classifier_path)
    feature_vector = read_feature_from_file(feature_file_path)
    feature_vector = [feature_vector]
    # scaler_path = rf_scaler_save_path
    # scaler = load_scaler(scaler_path)
    # feature_vector = scaler.transform([feature_vector])
    return predict_single_package(classifier, feature_vector)[0]
from .pickle_util import load_classifier, load_scaler
from .read_feature import read_feature_from_file
from .commons import MLP_path, rf_scaler_save_path, mlp_scaler_save_path, nb_path,nb_scaler_save_path, svm_scaler_save_path,svm_path, rf_classifier_path


def predict_single_package(classifier, feature_vec):
   return classifier.predict(feature_vec)

def predict_package_MLP(csv_path):
    classifier = load_classifier(MLP_path)
    feature_vec = read_feature_from_file(csv_path)
    scaler_path = mlp_scaler_save_path
    scaler = load_scaler(scaler_path)
    feature_vec = scaler.transform([feature_vec])
    return predict_single_package(classifier, feature_vec)[0]

def predict_package_NB(csv_path):
    classifier = load_classifier(nb_path)
    feature_vec = read_feature_from_file(csv_path)
    scaler_path = nb_scaler_save_path
    scaler = load_scaler(scaler_path)
    feature_vec = scaler.transform([feature_vec])
    return predict_single_package(classifier, feature_vec)[0]

def predict_package_SVM(csv_path):
    classifier = load_classifier(svm_path)
    feature_vec = read_feature_from_file(csv_path)
    scaler_path = svm_scaler_save_path
    scaler = load_scaler(scaler_path)
    feature_vec = scaler.transform([feature_vec])
    return predict_single_package(classifier, feature_vec)[0]

def predict_package_RF(csv_path):
    classifier = load_classifier(rf_classifier_path)
    feature_vec = read_feature_from_file(csv_path)
    feature_vec = [feature_vec]
    # scaler_path = rf_scaler_save_path
    # scaler = load_scaler(scaler_path)
    # feature_vec = scaler.transform([feature_vec])
    return predict_single_package(classifier, feature_vec)[0]
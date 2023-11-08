import os

from sklearn.metrics import accuracy_score, f1_score, make_scorer, matthews_corrcoef, precision_score, recall_score

from conf import SETTINGS


def getCurrentDir():
    return os.path.dirname(os.path.abspath(__file__))

table_path = os.path.join(getCurrentDir(), '..', 'results')

field_names = ["hyperparamter", "TP", "FP", "TN", "FN", "accuracy", "precision", "recall", "f1", "MCC"]

classifier_save_path = SETTINGS['path']['models']
rf_classifier_path = os.path.join(classifier_save_path, "RF.pkl")
MLP_path = os.path.join(classifier_save_path, "MLP.pkl")
nb_path = os.path.join(classifier_save_path, 'NB.pkl')
svm_path = os.path.join(classifier_save_path, 'SVM.pkl')

classifier_path = rf_classifier_path

scaler_save_path = SETTINGS['path']['models']
rf_scaler_save_path = os.path.join(scaler_save_path, 'RF_scaler.pkl')
mlp_scaler_save_path = os.path.join(scaler_save_path, 'MLP_scaler.pkl')
nb_scaler_save_path = os.path.join(scaler_save_path, 'NB_scaler.pkl')
svm_scaler_save_path = os.path.join(scaler_save_path, 'SVM_scaler.pkl')

scoring = {
    "prec": make_scorer(precision_score, pos_label="malicious"),
    "accu": make_scorer(accuracy_score),
    "rec": make_scorer(recall_score, pos_label="malicious"),
    "f1": make_scorer(f1_score, pos_label="malicious"),
    "matt_cor": make_scorer(matthews_corrcoef)
}
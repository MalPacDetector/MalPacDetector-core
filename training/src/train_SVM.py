import os

import numpy
from prettytable import PrettyTable
from sklearn.model_selection import StratifiedKFold, cross_validate, cross_val_predict
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC

from .commons import table_path, scoring, field_names, classifier_save_path
from .pickle_util import save_classifier
from conf import SETTINGS


def train_SVM_validate(X: numpy.ndarray, y: numpy.ndarray):
   """Train the SVM model and validate it using cross validation.
   
   Args:
      X: The training set.
      y: The labels of the training set.
   """
   gamma_arr = SETTINGS['classifier']['hyperparameters']['SVM']['gammas']
   C_arr = SETTINGS['classifier']['hyperparameters']['SVM']['C']
   k = 4
   skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=10)
   table = PrettyTable()
   csv_path = os.path.join(table_path, "SVM_validation.csv")
   table.field_names = field_names
   with open(csv_path, "w+") as f: 
      for C_val in C_arr:
         for gamma_val in gamma_arr:
               model = SVC(kernel="rbf", C=C_val, gamma=gamma_val)
               scores = cross_validate(model, X, y, cv= skf, scoring=scoring)
               y_pred = cross_val_predict(model, X, y, cv = skf)
               tn, fp, fn, tp = confusion_matrix(y, y_pred).ravel()
               table.add_row([f"c={C_val}; gamma_val={gamma_val};", tp, fp, tn, fn, scores["test_accu"].mean(), scores["test_prec"].mean(), scores["test_rec"].mean(), scores["test_f1"].mean(), scores["test_matt_cor"].mean()])
      f.write(table.get_csv_string())

def save_SVM(X_train: numpy.ndarray, y_train: numpy.ndarray, gamma: str or float, C: float):
   """Save the SVM model trained on the whole training set.

   Args:
      X_train: The training set.
      y_train: The labels of the training set.
      gamma: The gamma of the SVM.
      C: The C of the SVM.
   """
   model = SVC(C=C, gamma=gamma)
   model.fit(X_train, y_train)
   save_path = os.path.join(classifier_save_path, "SVM.pkl")
   save_classifier(model, save_path)
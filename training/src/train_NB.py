import os

import numpy
from sklearn.model_selection import StratifiedKFold, cross_validate, cross_val_predict
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB
from prettytable import PrettyTable

from .commons import field_names, table_path, scoring, classifier_save_path
from .pickle_util import save_classifier
from conf import SETTINGS


def train_NB_Validate(X_train: numpy.ndarray, y_train: numpy.ndarray):
   """Train the NB model and validate it using cross validation.
   
   Args:
      X_train: The training set.
      y_train: The labels of the training set.
   """
   table = PrettyTable()
   table.field_names = field_names
   csv_path = os.path.join(table_path, "NB_validation.csv")
   k = 4
   skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=10)
   smoothings = SETTINGS['classifier']['hyperparameters']['NB']['smoothings']
   with open(csv_path, "w+") as f:
      for smoothing in smoothings:
         model = GaussianNB(var_smoothing=smoothing)
         scores = cross_validate(model, X=X_train, y=y_train, cv=skf, scoring=scoring)
         y_pred = cross_val_predict(model, X_train, y_train, cv = skf)
         tn, fp, fn, tp = confusion_matrix(y_train, y_pred).ravel()
         table.add_row([f"smoothing={smoothing}", tp, fp, tn, fn, scores["test_accu"].mean(), scores["test_prec"].mean(), scores["test_rec"].mean(), scores["test_f1"].mean(), scores["test_matt_cor"].mean()])
      f.write(table.get_csv_string())

def save_NB(X_train: numpy.ndarray, y_train: numpy.ndarray, smoothing: float):
   """Save the NB model trained on the whole training set.
   
   Args:
      X_train: The training set.
      y_train: The labels of the training set.
      smoothing: The smoothing parameter of the NB.
   """
   save_path = os.path.join(classifier_save_path, "NB.pkl")
   model = GaussianNB(var_smoothing=smoothing)
   model.fit(X_train, y_train)
   save_classifier(model, save_path)
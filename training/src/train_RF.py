import os

import numpy
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_validate, cross_val_predict
from sklearn.metrics import confusion_matrix
from prettytable import PrettyTable

from .pickle_util import save_classifier
from .commons import table_path, field_names, classifier_save_path, scoring
from conf import SETTINGS


def train_classifier_RF_Validation(X: numpy.ndarray, y: numpy.ndarray):
   """Train the RF model and validate it using cross validation.
   
   Args:
      X: The training set.
      y: The labels of the training set.
   """
   number_of_decision_trees = SETTINGS['classifier']['hyperparameters']['RF']['number_of_decision_trees']
   maxium_depths = SETTINGS['classifier']['hyperparameters']['RF']['maxium_depths']

   k = 4
   skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=10)
   table_validate_path = os.path.join(table_path, "RF_validation.csv")

   validate_table = PrettyTable()
   validate_table.field_names = field_names

   with open(table_validate_path, "w+") as validate_file:
      for estimator in number_of_decision_trees:
            for depth in maxium_depths:
               model = RandomForestClassifier(n_estimators=estimator, max_depth=depth)
               scores = cross_validate(model, X, y, cv=skf,scoring=scoring)
               y_pred = cross_val_predict(model, X, y, cv = skf)
               tn, fp, fn, tp = confusion_matrix(y, y_pred).ravel()
               validate_table.add_row([f'estimators = {estimator}; max_depth={depth}', tp, fp, tn, fn, scores["test_accu"].mean(), scores["test_prec"].mean(), scores["test_rec"].mean(), scores["test_f1"].mean(), scores["test_matt_cor"].mean()])
      validate_file.write(validate_table.get_csv_string())

def save_RF(X_train: numpy.ndarray, y_train: numpy.ndarray, number_of_decision_trees: int, maxium_depth: int):
   """Save the RF model trained on the whole training set.
   
   Args:
      X_train: The training set.
      y_train: The labels of the training set.
      number_of_decision_trees: The number of decision trees of the RF.
      maxium_depth: The maxium depth of the RF.
   """
   model = RandomForestClassifier(n_estimators=number_of_decision_trees, max_depth=maxium_depth)
   model.fit(X_train, y_train)
   save_path = os.path.join(classifier_save_path, "RF.pkl")
   save_classifier(model, save_path)
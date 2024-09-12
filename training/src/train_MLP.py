import os

import numpy
from sklearn.model_selection import StratifiedKFold, cross_validate, cross_val_predict
from sklearn.metrics import confusion_matrix
from sklearn.neural_network import MLPClassifier
from prettytable import PrettyTable

from .commons import table_path, field_names,classifier_save_path, scoring
from .pickle_util import save_classifier
from conf import SETTINGS


def train_MLP_validation(X_train: numpy.ndarray, y_train: numpy.ndarray):
   """Train the MLP model and validate it using cross validation.
   
   Args:
      X_train: The training set.
      y_train: The labels of the training set.
   """
   layer_sizes = [(i,) for i in SETTINGS['classifier']['hyperparameters']['MLP']['number_of_hidden_units']]
   activations = SETTINGS['classifier']['hyperparameters']['MLP']['activation_functions']
   optimization_algorithms = SETTINGS['classifier']['hyperparameters']['MLP']['optimization_algorithms']
   learning_rates = SETTINGS['classifier']['hyperparameters']['MLP']['learning_rates']
   number_of_iterations = SETTINGS['classifier']['hyperparameters']['MLP']['number_of_iterations']

   table = PrettyTable()
   table.field_names = field_names
   validation_path = os.path.join(table_path, "MLP_validation.csv")

   k = 4
   skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=10)

   with open(validation_path, "w+") as f:
      for layer_size in layer_sizes:
         for activation in activations:
            for solver in optimization_algorithms:
               for learn_rate_init in learning_rates:
                  for max_iter in number_of_iterations:
                        model = MLPClassifier(hidden_layer_sizes=layer_size, solver=solver, random_state=21, max_iter=max_iter, learning_rate_init=learn_rate_init, activation=activation)
                        scores = cross_validate(model, X_train, y_train, cv=skf, scoring=scoring)
                        y_pred = cross_val_predict(model, X_train, y_train, cv = skf)
                        tn, fp, fn, tp = confusion_matrix(y_train, y_pred).ravel()
                        table.add_row([f'layer_size = {layer_size}; activation={activation}; solver={solver};learn_rate_int={learn_rate_init};max_iter={max_iter}',tp,fp,tn,fn, scores["test_accu"].mean(), scores["test_prec"].mean(), scores["test_rec"].mean(), scores["test_f1"].mean(), scores["test_matt_cor"].mean()])
      f.write(table.get_csv_string())

def save_MLP(X_train: numpy.ndarray, y_train: numpy.ndarray, learning_rate: float, number_of_hidden_units: tuple, number_of_iterations: int, optimization: str, activation: str):
   """Save the MLP model trained on the whole training set.

   Args:
      X_train: The training set.
      y_train: The labels of the training set.
      learning_rate: The learning rate of the MLP.
      number_of_hidden_units: The number of hidden units of the MLP.
      number_of_iterations: The number of iterations of the MLP.
      optimization: The optimization algorithm of the MLP.
      activation: The activation function of the MLP.
   """
   save_path = os.path.join(classifier_save_path, "MLP.pkl")
   model = MLPClassifier(hidden_layer_sizes=number_of_hidden_units, activation=activation, solver=optimization, learning_rate_init=learning_rate, max_iter=number_of_iterations)
   model.fit(X_train, y_train)
   save_classifier(model, save_path)
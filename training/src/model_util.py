from sklearn.metrics import accuracy_score, f1_score, matthews_corrcoef, precision_score, recall_score, confusion_matrix


def evaluate_model(y_test, y_pred):
   """Evaluate the model.

   Args:
      y_test (list): List of true labels.
      y_pred (list): List of predicted labels.
   """
   tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
   acc = accuracy_score(y_test, y_pred)
   precision = precision_score(y_test, y_pred, pos_label="malicious")
   recall = recall_score(y_test, y_pred, pos_label="malicious")
   f1 = f1_score(y_test, y_pred, pos_label="malicious")
   mcc = matthews_corrcoef(y_test, y_pred)
   return [tp, fp, tn, fn, acc, precision, recall, f1, mcc]
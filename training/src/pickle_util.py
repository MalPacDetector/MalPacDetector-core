import pickle


def save_classifier(classifier, file_path):
   with open(file_path, "wb") as f:
      pickle.dump(classifier, f)

def load_classifier(file_path):
   with open(file_path, "rb") as f:
      return pickle.load(f)

def save_scaler(scaler, scaler_save_path):
   with open(scaler_save_path, "wb") as f:
      pickle.dump(scaler, f)

def load_scaler(scaler_save_path):
   with open(scaler_save_path, "rb") as f:
      return pickle.load(f)
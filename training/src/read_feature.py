import csv
import os


def normalize_feature(value):
    if value == "true":
        value = True
    else:
        value = False
    return value

def read_feature_from_file(file_path):
   feature_vec = []
   with open(file_path, "r") as f:
      for row in csv.reader(f):
         _, value = row
         feature_vec.append(normalize_feature(value))
   return feature_vec

def read_features(malicousPath, normalPath):
    feature_arr = []
    label_arr = []
    csv_name_arr = []
    if malicousPath != None:
        read_features_from_di(malicousPath, feature_arr, label_arr, True, csv_name_arr)
    if normalPath != None:
        read_features_from_di(normalPath, feature_arr, label_arr, False, csv_name_arr)
    return [feature_arr, label_arr, csv_name_arr]

def read_features_from_di(dirPath, feature_arr: list, label_arr: list, isMalicous: bool, csv_name_arr: list):
    for root, _ , files in os.walk(dirPath):
        for f in files:
            csvPath = os.path.join(root, f)
            csv_name_arr.append(f)
            feature_arr.append(read_feature_from_file(csvPath))
            label_arr.append("malicious" if isMalicous  else "benign")
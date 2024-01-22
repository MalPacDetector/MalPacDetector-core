import csv
import os


def normalize_feature(value):
    """Normalize the feature value.
    
    Args:
        value: The feature value.

    Returns:
        The normalized feature value.
    """
    if value == "true":
        value = True
    elif value == "false":
        value = False
    return value

def read_feature_from_file(feature_file_path):
    """Read the feature from a file.

    Args:
        feature_file_path: The path of the feature file.

    Returns:
        The feature vector.
    """
    feature_vector = []
    with open(feature_file_path, "r") as f:
        for row in csv.reader(f):
            _, value = row
            feature_vector.append(normalize_feature(value))
    return feature_vector

def read_features(malicous_path, benign_path):
    """Read the features from the directory.
    
    Args:
        malicous_path: The path of the directory containing multiple malicious sample feature files.
        benign_path: The path of the directory containing multiple benign sample feature files.
    
    Returns:
        The features and labels.
    """
    feature_arr = []
    label_arr = []
    feature_file_names = []
    if malicous_path != None:
        read_features_from_di(malicous_path, feature_arr, label_arr, True, feature_file_names)
    if benign_path != None:
        read_features_from_di(benign_path, feature_arr, label_arr, False, feature_file_names)
    return [feature_arr, label_arr, feature_file_names]

def read_features_from_di(dirPath, feature_arr: list, label_arr: list, isMalicous: bool, feature_file_names: list):
    """Read the features from the directory.
    
    Args:
        dirPath: The path of the directory containing multiple sample feature files.
        feature_arr: The array to store the features.
        label_arr: The array to store the labels.
        isMalicous: Whether the samples are malicious.
        feature_file_names: The array to store the names of the feature files.

    Returns:
        The features and labels.
    """
    for root, _ , files in os.walk(dirPath):
        for f in files:
            csvPath = os.path.join(root, f)
            feature_file_names.append(f)
            feature_arr.append(read_feature_from_file(csvPath))
            label_arr.append("malicious" if isMalicous  else "benign")
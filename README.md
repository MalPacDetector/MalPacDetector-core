# MalPacDetector

This repository hosts dataset *MalnpmDB* and malicious package detector *MalPacDetector* involved in the paper *MalPacDetector: An LLM-based Malicious npm Package Detector*.

## Requirements
### Environment
- Operating System: Ubuntu 22.04
- Python: Python 3.10.12
- node.js: node.js v18.16.0

## Setup
```sh
$ python3 configure.py
```
Follow the tooltips to configure the project. You can configure:
- datasets path: Where to find npm packages. (default: datasets/MalnpmDB)
- models path: Where to save trained models. (default: models)
- reports path: Where to save prediction result reports. (default: reports)
- features: Where to save extracted features. (default: features)
- feature-positions: Where to save code line position information of extracted features. (default: feature-positions)

And, then use the following command to setup the project.
```sh
$ ./setup.sh
```

Once you setup the project, you will see the following folders:
- conf: containing configuration and settings files.
- datasets: containing MalnpmDB dataset.
- feature-extract: containing feature extraction code files.
- training: containing training and prediction code files.

If you using default configuration, you will see the following folders as well:
- models: containing trained machine learning models.
- reports: containing npm packages prediction reports.
- features: containing npm packages' features extracted by feature extractor.
- feature-positions: containing feature position information .

## Usage

At first, you should activate python virtual environment:
```sh
$ source env/bin/activate
```

And there is a main python script file:
- cli.py: for training a machine learning model and predicting npm packages. By specifying different paramaters, users can training different models or predicting different packages.

The paramaters available for performing a training or predicting task, which are listed below:

|Options|Description|
|---|---|
| -h | Show all help information. |
| extract | Extract features. |
| -h | Show help information about extracting features. |
| -d | npm dataset name. |
| train | Train model. |
| -h | Show help information about training models. |
| -m | Malicious npm dataset name. |
| -b | Benign npm dataset name. |
| -o | Model used to train. ("NB", "MLP", "RF", "SVM")|
| -p | Preprocess method. ("none", "standardlize", "min-max-scale")|
| -a | Trainging or saving model. (training, save) |
| -hs | smoothing of NB to save. |
| -hr | Learning rate of MLP to save. |
| -hl | Number of layers of MLP to save. |
| -hi | Number of iterations of MLP to save. |
| -ho | Optimization algorithm of MLP to save. |
| -ha | Activation funtion of MLP to save. |
| -he | Number of decision trees of RF to save. |
| -hd | Maxium depth of RF to save. |
| -hg | Gamma of SVM to save. |
| -hc | C of SVM to save. |
| predict | Predict npm packages. |
| -h | Show help information about predicting npm pacakges. |
| -o | Model used to predict. |
| -d | npm dataset which stored gzip formatted npm packages. |
| -p | npm package directory path. |

For convenience, use the following command to show help information.
```sh
# Show all help information.
$ python3 cli.py -h

# Show help information about extracting features.
$ python3 cli.py extract -h

# Show help information about training models.
$ python3 cli.py train -h

# Show help information about predicting npm dataset.
$ python3 cli.py predict -h
```

### Step 1: Extract features from npm dataset
The paramater related to model settings are presented in above table's field *extract*. The npm dataset should obey the following structure:

```sh
dataset_name
|__ <package_name-package_version1>.tar.gz
|__ <package_name-package_version2>.tar.gz
|__ ...
|__ <package_name-package_versionn>.tar.gz
```

The compressed package should have the following structure which is the formal npm structure:
```sh
package_name-package_version
|__ package
   |__ package.json
   |__ ...
```

Use the following command to extract features from npm dataset.
```sh
$ python3 cli.py extract -d <dataset_name>
```

### Step 2: Train a classifier
The paramater related to model settings are stored in `conf/settings.json`, and are presented in above table's field *train*. This allows user to conveniently train different models or use different datasets.

Use the following command to train a classifier.
```sh
$ python3 cli.py train -a training -m <malicious_dataset_name> -b <benign_dataset_name> -p <preprocess_method> -o <model_name>
```

### Step 3: Save the classifier
The paramater related to model settings are stored in `conf/settings.json`, and are presented in above table's field *train*.

Use the following command to train a classifier.
```sh
# NB
$ python3 cli.py train -a save -m <malicious_dataset_name> -b <benign_dataset_name> -p <preprocess_method> -o <model_name> -hs <smoothing>

# MLP
$ python3 cli.py train -a save -m <malicious_dataset_name> -b <benign_dataset_name> -p <preprocess_method> -o <model_name> -hr <learning_rate> -hl <number_of_layers> -hi <number_of_iterations> -ho <optimization_algorithm> -ha <activation_function>

# RF
$ python3 cli.py train -a save -m <malicious_dataset_name> -b <benign_dataset_name> -p <preprocess_method> -o <model_name> -he <number_of_decision_trees> -hd <maxium_depth>

# SVM
$ python3 cli.py train -a save -m <malicious_dataset_name> -b <benign_dataset_name> -p <preprocess_method> -o <model_name> -hg <Gamma> -hc <C>
```

### Step 4: Predict npm packages
The paramater related to model settings are presented in above table's field *predict*.

Use the following command to predict packages.
```sh
$ python3 cli.py predict -o <model_name> -d <dataset_name>
```

For convenience, you can just use one command to pass above steps to predict a single package.
```sh
$ python3 cli.py predict -o <model_name> -p <package_path>
```

## Hyperparameters
Hyperparameter values of the 4 classifiers, where
boldface means the best hyperparameter value of the model.
| Model | Hyperparameter |
| ---- | ---- |
| NB | Smoothing terms: (1e-9, 1e-8, 1e-7, 1e-6, 1e-5, **1e-4**) |
| MLP | Learning rate: 5 values randomly selected from a uniform distribution with the interval [0.01, 0.2] (**0.0505**)<br>Number of hidden units: (**16**, 32, 100, 150)<br>Number of iterations: (**400**, 600)<br>Optimization algorithm: (lbfgs, **adam**) |
| RF | Number of decision trees: (16, **32**, 64, 100, 128, 256, 512)<br>Maximum depth: (3, 5, 7, **11**, 15) |
| SVM | Gamma: (scale, auto, 3 values randomly selected from a normal distribution with mean 0.2 and standard deviation 0.075) (**scale**)<br>C: 3 values randomly selected from a uniform distribution with the [0.5, 2.0] (**1.0704**) |

## Dataset and Results
- Dataset: Containing malicious dataset *mal* and benign dataset *ben* in `datasets/MalnpmDB` which has 3258 and 4051 packages respectively.
- Training and Validation Results: Model training and validation results are stored in `trainging/result` directory, which named `***_validation.csv`, where `***` represents model name.

## Contact
Since the paper not having been published, and for security reasons, we can't place the malicious package dataset here. If you need the dataset, please send a request to **hust_jian@hust.edu.cn**.

Any bug report or improvement suggestions will be appreciated. Please kindly cite our paper if you use the code or data in your work.

Thanks!

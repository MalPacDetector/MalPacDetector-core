import os
import json


# project root path
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# load the settings
SETTINGS_PATH = os.path.join(ROOT_PATH, 'conf/settings.json')
try:
    with open(SETTINGS_PATH, 'r') as f:
        SETTINGS = json.load(f)
except FileNotFoundError:
    print(f'Error: {SETTINGS_PATH} not found!')
    exit(1)
except json.decoder.JSONDecodeError:
    print(f'Error: {SETTINGS_PATH} is not a valid json file!')
    exit(1)
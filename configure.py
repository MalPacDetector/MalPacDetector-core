import os
import json


def configure():
    """
    Configure the settings of the MalPacDetector.
    """
    print('Configuring the settings...')
    current_path = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(current_path, 'conf/settings.json')

    try:
        with open(settings_file_path, 'r') as f:
            current_settings = json.load(f)
    except FileNotFoundError:
        print(f'Error: {settings_file_path} not found!')
        exit(1)
    except json.decoder.JSONDecodeError:
        print(f'Error: {settings_file_path} is not a valid json file!')
        exit(1)
    
    print('Please configure the settings(Press Enter key to use current settings):')
    print('1. Configure the path of the datasets:')
    print(f'    Current path of the datasets: {current_settings["path"]["datasets"]}')
    print('    Enter the new path of the datasets:')
    datasets_path = input().strip()
    print('2. Configure the path of the models:')
    print(f'    Current path of the models: {current_settings["path"]["models"]}')
    print('    Enter the new path of the models:')
    models_path = input().strip()
    print('3. Configure the path of the reports:')
    print(f'    Current path of the reports: {current_settings["path"]["reports"]}')
    print('    Enter the new path of the reports:')
    reports_path = input().strip()
    print('4. Configure the path of the features:')
    print(f'    Current path of the features: {current_settings["path"]["features"]}')
    print('    Enter the new path of the features:')
    features_path = input().strip()
    print('5. Configure the path of the feature positions:')
    print(f'    Current path of the feature positions: {current_settings["path"]["feature-positions"]}')
    print('    Enter the new path of the feature positions:')
    feature_positions_path = input().strip()

    print('Saving the new settings...')
    current_settings['path']['datasets'] = datasets_path if datasets_path else current_settings["path"]['datasets']
    current_settings['path']['models'] = models_path if models_path else current_settings["path"]['models']
    current_settings['path']['reports'] = reports_path if reports_path else current_settings["path"]['reports']
    current_settings['path']['features'] = features_path if features_path else current_settings["path"]['features']
    current_settings['path']['feature-positions'] = feature_positions_path if feature_positions_path else current_settings["path"]['feature-positions']
    
    print('Creating the new directories...')
    os.makedirs(current_settings['path']['datasets'], exist_ok=True)
    os.makedirs(current_settings['path']['models'], exist_ok=True)
    os.makedirs(current_settings['path']['reports'], exist_ok=True)
    os.makedirs(current_settings['path']['features'], exist_ok=True)
    os.makedirs(current_settings['path']['feature-positions'], exist_ok=True)
    print('Creating the new directories successfully!')
    
    try:
        with open(settings_file_path, 'w') as f:
            json.dump(current_settings, f, indent=4)
    except FileNotFoundError:
        print(f'Error: {settings_file_path} not found!')
        exit(1)
    except json.decoder.JSONDecodeError:
        print(f'Error: {settings_file_path} is not a valid json file!')
        exit(1)
    print('Saving the new settings successfully!')
    print('Configure successfully!')

if __name__ == '__main__':
    print("""
 __  __         _  ____                ____         _                _                
|  \/  |  __ _ | ||  _ \   __ _   ___ |  _ \   ___ | |_   ___   ___ | |_   ___   _ __ 
| |\/| | / _` || || |_) | / _` | / __|| | | | / _ \| __| / _ \ / __|| __| / _ \ | '__|
| |  | || (_| || ||  __/ | (_| || (__ | |_| ||  __/| |_ |  __/| (__ | |_ | (_) || |   
|_|  |_| \__,_||_||_|     \__,_| \___||____/  \___| \__| \___| \___| \__| \___/ |_|   
""")
    configure()
import sys
import json
import boto3
import os
import logging


# Constants
AWS_PROFILE = 'ghactivity'
LOG_FILENAME = 'process_log.log'

# Set local path
project_path = os.getenv('MY_PROJECT_PATH')
if project_path:
    sys.path.append(project_path)
else:
    print("Environment variable MY_PROJECT_PATH is not set")


def get_parameter(name):
    """Retrieve a parameter from AWS SSM."""
    ssm = boto3.client('ssm')
    parameter = ssm.get_parameter(Name=name, WithDecryption=True)
    return parameter['Parameter']['Value']


def get_snowflake_credentials():
    """Get Snowflake credentials from AWS Parameter Store."""
    credentials = {
        "user": get_parameter('/sf_user'),
        "password": get_parameter('/sf_password'),
        "account": get_parameter('/sf_account'),
        "warehouse": get_parameter('/sf_warehouse'),
        "database": get_parameter('/sf_dbname'),
        "role": get_parameter('/sf_role')
    }
    return credentials


def read_config_old():
    with open('utils/config.json', 'r') as f:
        return json.load(f)
    


def read_config():
    config_path = 'utils/config.json'  # Update with the correct path
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"Config file not found at {config_path}")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Error parsing the config file at {config_path}")
        return {}



def setup_logging():
    """Set up logging for the application."""
    logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_aws_profile():
    """Initialize AWS profile environment variable."""
    os.environ.setdefault('AWS_PROFILE', AWS_PROFILE)


# Set local path
def add_project_path():
    project_path = os.getenv('MY_PROJECT_PATH')
    if project_path:
        sys.path.append(project_path)
    else:
        print("Environment variable MY_PROJECT_PATH is not set")
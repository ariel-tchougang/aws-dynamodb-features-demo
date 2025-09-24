import boto3
import json
import os

def load_config():
    """Load configuration from config.json file."""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

def get_dynamodb_client():
    """Create and return a DynamoDB client based on config.json settings."""
    config = load_config()
    
    session = boto3.Session(profile_name=config['aws_profile'])
    
    if config['dynamodb']['use_local_endpoint']:
        return session.client(
            'dynamodb',
            region_name=config['aws_region'],
            endpoint_url=config['dynamodb']['endpoint_url']
        )
    else:
        return session.client('dynamodb', region_name=config['aws_region'])

def get_dynamodb_resource():
    """Create and return a DynamoDB resource based on config.json settings."""
    config = load_config()
    
    session = boto3.Session(profile_name=config['aws_profile'])
    
    if config['dynamodb']['use_local_endpoint']:
        return session.resource(
            'dynamodb',
            region_name=config['aws_region'],
            endpoint_url=config['dynamodb']['endpoint_url']
        )
    else:
        return session.resource('dynamodb', region_name=config['aws_region'])
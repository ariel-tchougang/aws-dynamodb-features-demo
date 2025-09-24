import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.dynamodb_helper import get_dynamodb_resource

def create_game_leaderboard_table():
    dynamodb = get_dynamodb_resource()

    # Check if the table already exists
    existing_tables = dynamodb.tables
    if 'GameLeaderboard' in existing_tables:
        print("Table already exists.")
        return
    
    table = dynamodb.create_table(
        TableName='GameLeaderboard',
        KeySchema=[
            {
                'AttributeName': 'player_id',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'game_id',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'player_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'game_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'score',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'game_date',
                'AttributeType': 'S'
            }
        ],
        LocalSecondaryIndexes=[
            {
                'IndexName': 'ScoreIndex',
                'KeySchema': [
                    {
                        'AttributeName': 'player_id',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'score',
                        'KeyType': 'RANGE'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                }
            }
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'GameDateIndex',
                'KeySchema': [
                    {
                        'AttributeName': 'game_date',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'score',
                        'KeyType': 'RANGE'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 20,
            'WriteCapacityUnits': 20
        }
    )
    
    # Wait until the table exists
    table.meta.client.get_waiter('table_exists').wait(TableName='GameLeaderboard')
    print("Table created successfully!")
    return table

if __name__ == '__main__':
    create_game_leaderboard_table()
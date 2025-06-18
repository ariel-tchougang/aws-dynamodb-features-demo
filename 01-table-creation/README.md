# Lab 1: DynamoDB Table Creation

In this lab, you'll create a DynamoDB table for the Cosmic Defenders game leaderboard with a composite primary key, a Local Secondary Index (LSI), and a Global Secondary Index (GSI).

## Table Design

Our `GameLeaderboard` table will have the following structure:

- **Primary Key**:
  - Partition Key: `player_id` (String) - Unique identifier for each player
  - Sort Key: `game_id` (String) - Unique identifier for each game played

- **Local Secondary Index (LSI)**:
  - Name: `ScoreIndex`
  - Partition Key: `player_id` (Same as table's partition key)
  - Sort Key: `score` (Number) - Player's score in the game

- **Global Secondary Index (GSI)**:
  - Name: `GameDateIndex`
  - Partition Key: `game_date` (String) - Date of the game in ISO format (YYYY-MM-DD)
  - Sort Key: `score` (Number) - Player's score in the game

## Attributes

The table will include these attributes:
- `player_id` (String) - Unique player identifier
- `game_id` (String) - Unique game identifier
- `player_name` (String) - Player's display name
- `game_date` (String) - Date when the game was played
- `score` (Number) - Player's score in the game
- `game_duration` (Number) - Duration of the game in seconds
- `achievements` (List) - Achievements earned during the game
- `game_mode` (String) - Game mode (e.g., "battle-royale", "team-deathmatch")
- `expiration_time` (Number) - TTL attribute for data expiration
- `last_updated` (String) - Timestamp of the last update

## Instructions

### Option 1: Using AWS CLI

Run the following AWS CLI command to create the table:

```bash
aws dynamodb create-table \
    --table-name GameLeaderboard \
    --attribute-definitions \
        AttributeName=player_id,AttributeType=S \
        AttributeName=game_id,AttributeType=S \
        AttributeName=score,AttributeType=N \
        AttributeName=game_date,AttributeType=S \
    --key-schema \
        AttributeName=player_id,KeyType=HASH \
        AttributeName=game_id,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --local-secondary-indexes \
        "[{
            \"IndexName\": \"ScoreIndex\",
            \"KeySchema\": [
                {\"AttributeName\": \"player_id\", \"KeyType\": \"HASH\"},
                {\"AttributeName\": \"score\", \"KeyType\": \"RANGE\"}
            ],
            \"Projection\": {
                \"ProjectionType\": \"ALL\"
            }
        }]" \
    --global-secondary-indexes \
        "[{
            \"IndexName\": \"GameDateIndex\",
            \"KeySchema\": [
                {\"AttributeName\": \"game_date\", \"KeyType\": \"HASH\"},
                {\"AttributeName\": \"score\", \"KeyType\": \"RANGE\"}
            ],
            \"Projection\": {
                \"ProjectionType\": \"ALL\"
            },
            \"ProvisionedThroughput\": {
                \"ReadCapacityUnits\": 5,
                \"WriteCapacityUnits\": 5
            }
        }]"
```

### Option 2: Using Python with Boto3

```python
import boto3

def create_game_leaderboard_table():
    dynamodb = boto3.resource('dynamodb')
    
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
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    
    # Wait until the table exists
    table.meta.client.get_waiter('table_exists').wait(TableName='GameLeaderboard')
    print("Table created successfully!")
    return table

if __name__ == '__main__':
    create_game_leaderboard_table()
```

Save this code to a file named `create_table.py` and run it:

```bash
python create_table.py
```

## Verify Table Creation

Check if the table was created successfully:

```bash
aws dynamodb describe-table --table-name GameLeaderboard
```

## Next Steps

Once your table is created, proceed to [Lab 2: Data Loading](../02-data-loading/) to populate your table with game data.
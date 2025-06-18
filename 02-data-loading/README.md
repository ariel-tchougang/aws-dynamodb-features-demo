# Lab 2: Loading Data into DynamoDB

In this lab, you'll generate sample game data and load it into the `GameLeaderboard` table you created in Lab 1.

## Data Generation

We'll create a Python script to generate realistic game data for our Cosmic Defenders game. The script will:

1. Generate data for multiple players
2. Create multiple game records for each player
3. Include all required attributes for our table design
4. Save the data to a JSON file

## Instructions

### Step 1: Generate Sample Data

Run the provided Python script to generate sample game data:

```bash
python generate_data.py
```

This will create a file called `game_data.json` with sample game records.

### Step 2: Load Data into DynamoDB

After generating the data, you can load it into your DynamoDB table using one of the following methods:

#### Option 1: Using Python with Boto3

Run the provided Python script to load the data:

```bash
python load_data.py
```

#### Option 2: Using AWS CLI

You can also use the AWS CLI to load individual items:

```bash
aws dynamodb put-item \
    --table-name GameLeaderboard \
    --item file://item.json
```

## Data Structure

Each game record will have the following structure:

```json
{
  "player_id": "p123456",
  "game_id": "g789012",
  "player_name": "CosmicWarrior",
  "game_date": "2023-05-15",
  "score": 8750,
  "game_duration": 345,
  "achievements": ["FirstBlood", "TripleKill"],
  "game_mode": "battle-royale",
  "expiration_time": 1715644800,
  "last_updated": "2023-05-15T14:30:45Z"
}
```

## Verify Data Loading

To verify that your data was loaded successfully, you can run a scan operation:

```bash
aws dynamodb scan --table-name GameLeaderboard --limit 5
```

This will return the first 5 items from your table.

## Next Steps

Once your data is loaded, proceed to [Lab 3: CRUD Operations](../03-crud-operations/) to learn how to perform basic operations on your DynamoDB table.
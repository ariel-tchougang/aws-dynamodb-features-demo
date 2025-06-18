import boto3
import time

def create_player_inventory_table():
    """Create the PlayerInventory table for transaction demo."""
    
    dynamodb = boto3.resource('dynamodb')
    
    # Check if table already exists
    existing_tables = [table.name for table in dynamodb.tables.all()]
    if 'PlayerInventory' in existing_tables:
        print("PlayerInventory table already exists.")
        return dynamodb.Table('PlayerInventory')
    
    # Create table
    table = dynamodb.create_table(
        TableName='PlayerInventory',
        KeySchema=[
            {
                'AttributeName': 'player_id',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'item_id',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'player_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'item_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    
    # Wait until the table exists
    table.meta.client.get_waiter('table_exists').wait(TableName='PlayerInventory')
    print("PlayerInventory table created successfully!")
    return table

def create_game_achievements_table():
    """Create the GameAchievements table for transaction demo."""
    
    dynamodb = boto3.resource('dynamodb')
    
    # Check if table already exists
    existing_tables = [table.name for table in dynamodb.tables.all()]
    if 'GameAchievements' in existing_tables:
        print("GameAchievements table already exists.")
        return dynamodb.Table('GameAchievements')
    
    # Create table
    table = dynamodb.create_table(
        TableName='GameAchievements',
        KeySchema=[
            {
                'AttributeName': 'player_id',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'achievement_id',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'player_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'achievement_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    
    # Wait until the table exists
    table.meta.client.get_waiter('table_exists').wait(TableName='GameAchievements')
    print("GameAchievements table created successfully!")
    return table

def load_sample_data():
    """Load sample data into the transaction tables."""
    
    dynamodb = boto3.resource('dynamodb')
    player_inventory = dynamodb.Table('PlayerInventory')
    game_achievements = dynamodb.Table('GameAchievements')
    
    print("Loading sample data...")
    
    # Add player currency items
    player_inventory.put_item(
        Item={
            'player_id': 'player1',
            'item_id': 'currency',
            'item_name': 'Cosmic Coins',
            'quantity': 1000,
            'last_updated': time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    )
    
    player_inventory.put_item(
        Item={
            'player_id': 'player2',
            'item_id': 'currency',
            'item_name': 'Cosmic Coins',
            'quantity': 500,
            'last_updated': time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    )
    
    # Add some inventory items
    player_inventory.put_item(
        Item={
            'player_id': 'player1',
            'item_id': 'item_001',
            'item_name': 'Plasma Sword',
            'quantity': 1,
            'rarity': 'Rare',
            'last_updated': time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    )
    
    player_inventory.put_item(
        Item={
            'player_id': 'player2',
            'item_id': 'item_002',
            'item_name': 'Shield Generator',
            'quantity': 1,
            'rarity': 'Epic',
            'last_updated': time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    )
    
    # Add some achievements
    game_achievements.put_item(
        Item={
            'player_id': 'player1',
            'achievement_id': 'ach_001',
            'achievement_name': 'First Victory',
            'unlocked_date': time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'reward_claimed': False
        }
    )
    
    game_achievements.put_item(
        Item={
            'player_id': 'player2',
            'achievement_id': 'ach_002',
            'achievement_name': 'Sharpshooter',
            'unlocked_date': time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'reward_claimed': False
        }
    )
    
    print("Sample data loaded successfully!")

def setup_transaction_tables():
    """Set up tables and data for transaction demo."""
    
    print("Setting up tables for transaction demo...")
    
    # Create tables
    create_player_inventory_table()
    create_game_achievements_table()
    
    # Load sample data
    load_sample_data()
    
    print("Setup complete!")

if __name__ == "__main__":
    setup_transaction_tables()
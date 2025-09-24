import sys
import os
import time
from botocore.exceptions import ClientError
from decimal import Decimal
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.dynamodb_helper import get_dynamodb_client

def award_achievement_reward(player_id, achievement_id):
    """Award achievement reward using a transaction."""
    
    dynamodb = get_dynamodb_client()
    
    try:
        print(f"\nAwarding achievement reward to player {player_id}...")
        
        response = dynamodb.transact_write_items(
            TransactItems=[
                # Check if achievement exists and is unclaimed
                {
                    'Update': {
                        'TableName': 'GameAchievements',
                        'Key': {
                            'player_id': {'S': player_id},
                            'achievement_id': {'S': achievement_id}
                        },
                        'UpdateExpression': 'SET reward_claimed = :claimed',
                        'ConditionExpression': 'attribute_exists(player_id) AND reward_claimed = :unclaimed',
                        'ExpressionAttributeValues': {
                            ':claimed': {'BOOL': True},
                            ':unclaimed': {'BOOL': False}
                        }
                    }
                },
                # Add reward currency to player
                {
                    'Update': {
                        'TableName': 'PlayerInventory',
                        'Key': {
                            'player_id': {'S': player_id},
                            'item_id': {'S': 'currency'}
                        },
                        'UpdateExpression': 'ADD quantity :reward',
                        'ExpressionAttributeValues': {
                            ':reward': {'N': '100'}
                        }
                    }
                }
            ]
        )
        
        print("Achievement reward awarded successfully!")
        print("- Achievement marked as claimed")
        print("- 100 Cosmic Coins added to player inventory")
        return True
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'TransactionCanceledException':
            print("Transaction cancelled:")
            print("- Achievement might not exist")
            print("- Achievement might already be claimed")
            print("- Player might not have a currency record")
        else:
            print(f"Error: {e.response['Error']['Message']}")
        return False

def transfer_item(from_player, to_player, item_id):
    """Transfer an item between players using a transaction."""
    
    dynamodb = get_dynamodb_client()
    
    try:
        print(f"\nTransferring item {item_id} from {from_player} to {to_player}...")
        
        response = dynamodb.transact_write_items(
            TransactItems=[
                # Remove item from sender
                {
                    'Delete': {
                        'TableName': 'PlayerInventory',
                        'Key': {
                            'player_id': {'S': from_player},
                            'item_id': {'S': item_id}
                        },
                        'ConditionExpression': 'attribute_exists(player_id)'
                    }
                },
                # Add item to receiver
                {
                    'Put': {
                        'TableName': 'PlayerInventory',
                        'Item': {
                            'player_id': {'S': to_player},
                            'item_id': {'S': item_id},
                            'item_name': {'S': 'Transferred Item'},
                            'quantity': {'N': '1'},
                            'last_updated': {'S': time.strftime("%Y-%m-%dT%H:%M:%SZ")}
                        },
                        'ConditionExpression': 'attribute_not_exists(player_id) OR attribute_not_exists(item_id)'
                    }
                }
            ]
        )
        
        print("Item transferred successfully!")
        return True
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'TransactionCanceledException':
            print("Transaction cancelled:")
            print("- Source item might not exist")
            print("- Destination might already have an item with same ID")
        else:
            print(f"Error: {e.response['Error']['Message']}")
        return False

def read_player_state(player_id):
    """Read player's inventory and achievements atomically."""
    
    dynamodb = get_dynamodb_client()
    
    try:
        print(f"\nReading state for player {player_id}...")
        
        response = dynamodb.transact_get_items(
            TransactItems=[
                {
                    'Get': {
                        'TableName': 'PlayerInventory',
                        'Key': {
                            'player_id': {'S': player_id},
                            'item_id': {'S': 'currency'}
                        }
                    }
                },
                {
                    'Get': {
                        'TableName': 'GameAchievements',
                        'Key': {
                            'player_id': {'S': player_id},
                            'achievement_id': {'S': 'ach_001'}
                        }
                    }
                }
            ]
        )
        
        print("\nPlayer state:")
        for item in response['Responses']:
            if 'Item' in item:
                if 'quantity' in item['Item']:
                    print(f"- Currency balance: {item['Item']['quantity']['N']}")
                if 'achievement_name' in item['Item']:
                    print(f"- Achievement: {item['Item']['achievement_name']['S']}")
                    print(f"- Claimed: {item['Item']['reward_claimed']['BOOL']}")
        
        return True
        
    except ClientError as e:
        print(f"Error: {e.response['Error']['Message']}")
        return False

def run_transaction_demo():
    """Run various transaction examples."""
    
    print("=== DynamoDB Transactions Demo ===")
    
    # Award achievement reward
    award_achievement_reward('player1', 'ach_001')
    
    # Transfer item between players
    transfer_item('player1', 'player2', 'item_001')
    
    # Read player state
    read_player_state('player1')

if __name__ == "__main__":
    run_transaction_demo()
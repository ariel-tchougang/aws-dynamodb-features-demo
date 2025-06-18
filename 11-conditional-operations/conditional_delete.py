import boto3
import time
import uuid
from decimal import Decimal
from botocore.exceptions import ClientError

def create_test_item():
    """Create a test item for conditional delete demonstration."""
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    # Generate unique IDs
    player_id = f"del-{uuid.uuid4().hex[:8]}"
    game_id = f"del-{uuid.uuid4().hex[:8]}"
    
    # Create item
    item = {
        'player_id': player_id,
        'game_id': game_id,
        'player_name': 'DeleteTestPlayer',
        'score': Decimal('1500'),
        'game_mode': 'test-mode',
        'game_date': time.strftime("%Y-%m-%d"),
        'last_updated': time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    
    table.put_item(Item=item)
    print(f"Created test item: {player_id}/{game_id}")
    
    return player_id, game_id

def conditional_delete_by_score():
    """Demonstrate conditional delete based on score threshold."""
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    # Create test item
    player_id, game_id = create_test_item()
    
    print(f"\n=== Conditional Delete: Delete Only If Score < 2000 ===")
    
    try:
        # Delete with condition that score is less than 2000
        response = table.delete_item(
            Key={
                'player_id': player_id,
                'game_id': game_id
            },
            ConditionExpression='score < :threshold',
            ExpressionAttributeValues={
                ':threshold': Decimal('2000')
            },
            ReturnValues='ALL_OLD'
        )
        
        print("Item deleted successfully!")
        print("Deleted item had these attributes:")
        for key, value in response['Attributes'].items():
            print(f"  {key}: {value}")
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print("Delete failed: Score is not less than 2000.")
        else:
            print(f"Error: {e.response['Error']['Message']}")

def conditional_delete_by_attribute():
    """Demonstrate conditional delete based on attribute existence."""
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    # Create test items
    player_id1, game_id1 = create_test_item()
    player_id2, game_id2 = create_test_item()
    
    # Add a "test_flag" attribute to the first item
    table.update_item(
        Key={
            'player_id': player_id1,
            'game_id': game_id1
        },
        UpdateExpression='SET test_flag = :val',
        ExpressionAttributeValues={
            ':val': True
        }
    )
    
    print(f"\n=== Conditional Delete: Delete Only If Attribute Exists ===")
    
    # Try to delete first item (should succeed)
    print(f"\nAttempting to delete item with test_flag attribute...")
    try:
        response = table.delete_item(
            Key={
                'player_id': player_id1,
                'game_id': game_id1
            },
            ConditionExpression='attribute_exists(test_flag)',
            ReturnValues='ALL_OLD'
        )
        
        print("Item deleted successfully!")
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print("Delete failed: test_flag attribute does not exist.")
        else:
            print(f"Error: {e.response['Error']['Message']}")
    
    # Try to delete second item (should fail)
    print(f"\nAttempting to delete item without test_flag attribute...")
    try:
        response = table.delete_item(
            Key={
                'player_id': player_id2,
                'game_id': game_id2
            },
            ConditionExpression='attribute_exists(test_flag)',
            ReturnValues='ALL_OLD'
        )
        
        print("Item deleted successfully!")
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print("Delete failed as expected: test_flag attribute does not exist.")
        else:
            print(f"Error: {e.response['Error']['Message']}")
    
    # Clean up the second item
    table.delete_item(
        Key={
            'player_id': player_id2,
            'game_id': game_id2
        }
    )

if __name__ == "__main__":
    print("=== Conditional Delete Operations Demo ===")
    conditional_delete_by_score()
    conditional_delete_by_attribute()
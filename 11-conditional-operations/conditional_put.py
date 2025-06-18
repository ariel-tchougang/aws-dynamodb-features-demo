import boto3
import time
import uuid
from decimal import Decimal
from botocore.exceptions import ClientError

def conditional_put_new_item():
    """Demonstrate conditional put to create an item only if it doesn't exist."""
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    # Generate unique IDs
    player_id = f"cond-{uuid.uuid4().hex[:8]}"
    game_id = f"cond-{uuid.uuid4().hex[:8]}"
    
    print(f"=== Conditional Put: Create Only If Not Exists ===")
    print(f"Attempting to create new item: {player_id}/{game_id}")
    
    # New item to create
    new_item = {
        'player_id': player_id,
        'game_id': game_id,
        'player_name': 'ConditionalPlayer',
        'score': Decimal('5000'),
        'game_date': time.strftime("%Y-%m-%d"),
        'last_updated': time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    
    try:
        # Put with condition that the item doesn't already exist
        response = table.put_item(
            Item=new_item,
            ConditionExpression='attribute_not_exists(player_id)',
            ReturnValues='ALL_OLD'
        )
        
        print("Item created successfully!")
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print("Item already exists! Conditional put failed.")
        else:
            print(f"Error: {e.response['Error']['Message']}")
    
    # Try again with the same item (should fail)
    print("\nTrying to create the same item again...")
    
    try:
        response = table.put_item(
            Item=new_item,
            ConditionExpression='attribute_not_exists(player_id)',
            ReturnValues='ALL_OLD'
        )
        
        print("Item created successfully!")
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print("Item already exists! Conditional put failed as expected.")
        else:
            print(f"Error: {e.response['Error']['Message']}")

def conditional_put_with_value_check():
    """Demonstrate conditional put based on attribute value."""
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    # Generate unique IDs
    player_id = f"cond-{uuid.uuid4().hex[:8]}"
    game_id = f"cond-{uuid.uuid4().hex[:8]}"
    
    print(f"\n=== Conditional Put: Update Only If Score Is Lower ===")
    
    # Create initial item
    initial_item = {
        'player_id': player_id,
        'game_id': game_id,
        'player_name': 'HighScorePlayer',
        'score': Decimal('3000'),
        'game_date': time.strftime("%Y-%m-%d"),
        'last_updated': time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    
    print(f"Creating initial item with score: {initial_item['score']}")
    table.put_item(Item=initial_item)
    
    # Try to update with higher score (should succeed)
    higher_score_item = initial_item.copy()
    higher_score_item['score'] = Decimal('4000')
    higher_score_item['last_updated'] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    print(f"\nAttempting to update with higher score: {higher_score_item['score']}")
    
    try:
        response = table.put_item(
            Item=higher_score_item,
            ConditionExpression='attribute_not_exists(player_id) OR score < :new_score',
            ExpressionAttributeValues={
                ':new_score': higher_score_item['score']
            },
            ReturnValues='ALL_OLD'
        )
        
        print("Update successful! New high score recorded.")
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print("Update failed: New score is not higher than existing score.")
        else:
            print(f"Error: {e.response['Error']['Message']}")
    
    # Try to update with lower score (should fail)
    lower_score_item = initial_item.copy()
    lower_score_item['score'] = Decimal('2000')
    lower_score_item['last_updated'] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    print(f"\nAttempting to update with lower score: {lower_score_item['score']}")
    
    try:
        response = table.put_item(
            Item=lower_score_item,
            ConditionExpression='attribute_not_exists(player_id) OR score < :new_score',
            ExpressionAttributeValues={
                ':new_score': lower_score_item['score']
            },
            ReturnValues='ALL_OLD'
        )
        
        print("Update successful!")
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print("Update failed as expected: New score is lower than existing score.")
        else:
            print(f"Error: {e.response['Error']['Message']}")

if __name__ == "__main__":
    print("=== Conditional Put Operations Demo ===")
    conditional_put_new_item()
    conditional_put_with_value_check()
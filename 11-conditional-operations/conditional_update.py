import boto3
import time
import uuid
from decimal import Decimal
from botocore.exceptions import ClientError

def create_player_profile():
    """Create a player profile with version number for optimistic locking."""
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    player_id = f"cond-{uuid.uuid4().hex[:8]}"
    
    # Initial player profile
    player_profile = {
        'player_id': player_id,
        'game_id': 'profile',
        'player_name': 'OptimisticPlayer',
        'score': Decimal('1000'),
        'rank': 'Bronze',
        'version': 1,  # Initial version
        'last_updated': time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    
    # Create the profile
    table.put_item(Item=player_profile)
    
    print(f"Created player profile: {player_id}")
    print("Initial profile:")
    print(f"- Name: {player_profile['player_name']}")
    print(f"- Score: {player_profile['score']}")
    print(f"- Rank: {player_profile['rank']}")
    print(f"- Version: {player_profile['version']}")
    
    return player_id

def update_with_optimistic_locking(player_id, new_score, expected_version):
    """Update player score with optimistic locking using version number."""
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    # Calculate new rank based on score
    new_rank = 'Bronze'
    if new_score >= 5000:
        new_rank = 'Diamond'
    elif new_score >= 3000:
        new_rank = 'Platinum'
    elif new_score >= 2000:
        new_rank = 'Gold'
    elif new_score >= 1000:
        new_rank = 'Silver'
    
    try:
        # Update with condition on version
        response = table.update_item(
            Key={
                'player_id': player_id,
                'game_id': 'profile'
            },
            UpdateExpression='SET score = :score, rank = :rank, version = :new_version, last_updated = :timestamp',
            ConditionExpression='version = :expected_version',
            ExpressionAttributeValues={
                ':score': Decimal(str(new_score)),
                ':rank': new_rank,
                ':new_version': expected_version + 1,
                ':expected_version': expected_version,
                ':timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ")
            },
            ReturnValues='ALL_NEW'
        )
        
        updated_profile = response['Attributes']
        
        print(f"\nSuccessfully updated player profile:")
        print(f"- Score: {updated_profile['score']}")
        print(f"- Rank: {updated_profile['rank']}")
        print(f"- Version: {updated_profile['version']}")
        
        return True, updated_profile['version']
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print("\nUpdate failed: Version mismatch!")
            print("Another process may have updated this profile.")
            
            # Get current version
            response = table.get_item(
                Key={
                    'player_id': player_id,
                    'game_id': 'profile'
                }
            )
            
            if 'Item' in response:
                current_version = response['Item']['version']
                print(f"Current version is: {current_version}, but expected: {expected_version}")
            
            return False, None
        else:
            print(f"Error: {e.response['Error']['Message']}")
            return False, None

def simulate_concurrent_updates():
    """Simulate concurrent updates to demonstrate optimistic locking."""
    
    # Create a new player profile
    player_id = create_player_profile()
    
    print("\n=== Simulating concurrent updates ===")
    
    # First update - should succeed
    print("\nUpdate 1: Increasing score to 1500")
    success, version = update_with_optimistic_locking(player_id, 1500, 1)
    
    if success:
        # Second update with correct version - should succeed
        print("\nUpdate 2: Increasing score to 2500 with correct version")
        success, version = update_with_optimistic_locking(player_id, 2500, 2)
        
        # Third update with incorrect version - should fail
        print("\nUpdate 3: Trying to update with incorrect version")
        success, _ = update_with_optimistic_locking(player_id, 3500, 1)  # Using old version
        
        if not success:
            # Fourth update with correct version - should succeed
            print("\nUpdate 4: Retrying with correct version")
            success, version = update_with_optimistic_locking(player_id, 3500, 3)

if __name__ == "__main__":
    print("=== Conditional Update with Optimistic Locking Demo ===")
    simulate_concurrent_updates()
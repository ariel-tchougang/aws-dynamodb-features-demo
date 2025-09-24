import sys
import os
from decimal import Decimal
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.dynamodb_helper import get_dynamodb_resource

def put_item():
    """Create a new game record in the GameLeaderboard table."""
    
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table('GameLeaderboard')
    
    # Start timing
    start_time = time.time()
    
    # Put item operation
    response = table.put_item(
        Item={
            'player_id': 'p12345678',
            'game_id': 'g87654321',
            'player_name': 'NewPlayer123',
            'game_date': '2023-06-01',
            'score': Decimal('9500'),
            'game_duration': Decimal('450'),
            'achievements': ['FirstBlood', 'Survivor'],
            'game_mode': 'battle-royale',
            'expiration_time': Decimal('0'),
            'last_updated': '2023-06-01T10:15:30Z'
        }
    )
    
    # Calculate execution time
    execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    print(f"Put Item succeeded in {execution_time:.2f} ms")
    print(f"HTTP Status Code: {response['ResponseMetadata']['HTTPStatusCode']}")
    print(f"Request ID: {response['ResponseMetadata']['RequestId']}")
    
    # Return the item we just created for verification
    get_response = table.get_item(
        Key={
            'player_id': 'p12345678',
            'game_id': 'g87654321'
        }
    )
    
    if 'Item' in get_response:
        print("\nVerification - Item created:")
        for key, value in get_response['Item'].items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    put_item()
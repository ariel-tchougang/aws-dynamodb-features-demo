import sys
import os
import json
from decimal import Decimal
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.dynamodb_helper import get_dynamodb_resource

class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert Decimal to float for JSON serialization."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def get_item():
    """Retrieve a specific game record from the GameLeaderboard table."""
    
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table('GameLeaderboard')
    
    # Start timing
    start_time = time.time()
    
    # Get item operation
    response = table.get_item(
        Key={
            'player_id': 'p12345678',
            'game_id': 'g87654321'
        }
    )
    
    # Calculate execution time
    execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    print(f"Get Item executed in {execution_time:.2f} ms")
    print(f"HTTP Status Code: {response['ResponseMetadata']['HTTPStatusCode']}")
    print(f"Request ID: {response['ResponseMetadata']['RequestId']}")
    
    # Display the retrieved item
    if 'Item' in response:
        print("\nItem retrieved:")
        print(json.dumps(response['Item'], indent=2, cls=DecimalEncoder))
    else:
        print("\nItem not found")

if __name__ == "__main__":
    get_item()
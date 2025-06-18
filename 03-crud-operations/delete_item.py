import boto3
import json
from decimal import Decimal
import time

class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert Decimal to float for JSON serialization."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def delete_item():
    """Delete a game record from the GameLeaderboard table."""
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    # Start timing
    start_time = time.time()
    
    # Delete item operation
    response = table.delete_item(
        Key={
            'player_id': 'p12345678',
            'game_id': 'g87654321'
        },
        ReturnValues="ALL_OLD"
    )
    
    # Calculate execution time
    execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    print(f"Delete Item executed in {execution_time:.2f} ms")
    print(f"HTTP Status Code: {response['ResponseMetadata']['HTTPStatusCode']}")
    print(f"Request ID: {response['ResponseMetadata']['RequestId']}")
    
    # Display the deleted item
    if 'Attributes' in response:
        print("\nDeleted item:")
        print(json.dumps(response['Attributes'], indent=2, cls=DecimalEncoder))
    else:
        print("\nItem not found or already deleted")
    
    # Verify deletion
    verify_response = table.get_item(
        Key={
            'player_id': 'p12345678',
            'game_id': 'g87654321'
        }
    )
    
    if 'Item' not in verify_response:
        print("\nVerification successful: Item no longer exists in the table")
    else:
        print("\nVerification failed: Item still exists in the table")

if __name__ == "__main__":
    delete_item()
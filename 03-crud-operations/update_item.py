import boto3
import json
from decimal import Decimal
from datetime import datetime
import time

class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert Decimal to float for JSON serialization."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def update_item():
    """Update an existing game record in the GameLeaderboard table."""
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    # Current timestamp for the update
    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Start timing
    start_time = time.time()
    
    # Update item operation
    response = table.update_item(
        Key={
            'player_id': 'p12345678',
            'game_id': 'g87654321'
        },
        UpdateExpression="SET score = :s, achievements = :a, last_updated = :lu",
        ExpressionAttributeValues={
            ':s': Decimal('9800'),
            ':a': ['FirstBlood', 'Survivor', 'MVP'],
            ':lu': current_time
        },
        ReturnValues="ALL_NEW"
    )
    
    # Calculate execution time
    execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    print(f"Update Item executed in {execution_time:.2f} ms")
    print(f"HTTP Status Code: {response['ResponseMetadata']['HTTPStatusCode']}")
    print(f"Request ID: {response['ResponseMetadata']['RequestId']}")
    
    # Display the updated item
    if 'Attributes' in response:
        print("\nUpdated item:")
        print(json.dumps(response['Attributes'], indent=2, cls=DecimalEncoder))
    else:
        print("\nUpdate failed or item not found")

if __name__ == "__main__":
    update_item()
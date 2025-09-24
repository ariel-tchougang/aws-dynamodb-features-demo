import sys
import os
import json
import time
from decimal import Decimal
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.dynamodb_helper import get_dynamodb_resource

class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert Decimal to float for JSON serialization."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def scan_with_projection():
    """Demonstrate scan with projection expression to retrieve only specific attributes."""
    
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table('GameLeaderboard')
    
    print("=== Scan with Projection Expression ===")
    print("Retrieving only player_id, player_name, and score attributes")
    
    # Start timing
    start_time = time.time()
    
    # Scan with projection expression
    response = table.scan(
        ProjectionExpression="player_id, player_name, score",
        ReturnConsumedCapacity='TOTAL'
    )
    
    # Calculate execution time
    execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    # Print results
    print(f"\nScan executed in {execution_time:.2f} ms")
    print(f"Items retrieved: {len(response['Items'])}")
    print(f"Consumed capacity: {response['ConsumedCapacity']['CapacityUnits']} RCUs")
    
    # Show sample items with projected attributes
    print("\n=== Sample Items (with only projected attributes) ===")
    for item in response['Items'][:5]:  # Show first 5 items
        print(json.dumps(item, indent=2, cls=DecimalEncoder))
    
    print("\n=== Projection Benefits ===")
    print("Projections reduce the amount of data transferred from DynamoDB")
    print("This can improve performance and reduce consumed read capacity")
    print("Especially useful when items have many attributes but you only need a few")
    print("Note: You are still charged for reading the entire item from disk")

if __name__ == "__main__":
    scan_with_projection()
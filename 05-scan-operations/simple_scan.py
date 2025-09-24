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

def simple_scan():
    """Demonstrate a simple scan operation on a DynamoDB table."""
    
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table('GameLeaderboard')
    
    print("=== Simple Scan Operation ===")
    
    # Start timing
    start_time = time.time()
    
    # Perform a simple scan
    response = table.scan(
        ReturnConsumedCapacity='TOTAL'
    )
    
    # Calculate execution time
    execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    # Print results
    print(f"\nScan executed in {execution_time:.2f} ms")
    print(f"Items retrieved: {len(response['Items'])}")
    print(f"Consumed capacity: {response['ConsumedCapacity']['CapacityUnits']} RCUs")
    
    # Show sample items
    print("\n=== Sample Items ===")
    for item in response['Items'][:3]:  # Show first 3 items
        print(json.dumps(item, indent=2, cls=DecimalEncoder))

if __name__ == "__main__":
    simple_scan()
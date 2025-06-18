import boto3
import json
import time
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert Decimal to float for JSON serialization."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def scan_with_max_items():
    """Demonstrate scan with a maximum number of items limit."""
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    print("=== Scan with Max Items ===")
    print("Limiting scan to 20 items maximum")
    
    # Start timing
    start_time = time.time()
    
    # Scan with max items limit
    response = table.scan(
        ReturnConsumedCapacity='TOTAL',
        Limit=20  # Limit to 20 items
    )
    
    # Calculate execution time
    execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    # Print results
    print(f"\nScan executed in {execution_time:.2f} ms")
    print(f"Items retrieved: {len(response['Items'])}")
    print(f"Consumed capacity: {response['ConsumedCapacity']['CapacityUnits']} RCUs")
    
    # Check if we have more items
    if 'LastEvaluatedKey' in response:
        print("\n=== Continuation Token ===")
        print("Not all items retrieved. LastEvaluatedKey:")
        print(json.dumps(response['LastEvaluatedKey'], cls=DecimalEncoder))
        print("\nUse this key with ExclusiveStartKey to continue the scan")
    else:
        print("\nAll items retrieved (less than max items limit)")
    
    # Show sample items
    print("\n=== Sample Items ===")
    for item in response['Items'][:3]:  # Show first 3 items
        print(json.dumps(item, indent=2, cls=DecimalEncoder))
    
    print("\n=== Max Items Usage ===")
    print("Use max items when you want to process data in batches")
    print("or when you want to limit the amount of data returned in a single operation.")

if __name__ == "__main__":
    scan_with_max_items()
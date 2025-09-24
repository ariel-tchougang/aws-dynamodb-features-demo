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

def scan_with_starting_token():
    """Demonstrate scan with a starting token (continuation from a previous scan)."""
    
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table('GameLeaderboard')
    
    print("=== Scan with Starting Token ===")
    
    # First scan to get a starting token
    print("\n--- First Scan (20 items) ---")
    start_time = time.time()
    
    response = table.scan(
        ReturnConsumedCapacity='TOTAL',
        Limit=20
    )
    
    execution_time = (time.time() - start_time) * 1000
    print(f"First scan executed in {execution_time:.2f} ms")
    print(f"Items retrieved: {len(response['Items'])}")
    print(f"Consumed capacity: {response['ConsumedCapacity']['CapacityUnits']} RCUs")
    
    # Check if we have more items
    if 'LastEvaluatedKey' in response:
        last_key = response['LastEvaluatedKey']
        print("\n--- Continuation Token ---")
        print("LastEvaluatedKey:")
        print(json.dumps(last_key, cls=DecimalEncoder))
        
        # Continue scan with the LastEvaluatedKey
        print("\n--- Second Scan (with LastEvaluatedKey) ---")
        start_time = time.time()
        
        response2 = table.scan(
            ExclusiveStartKey=last_key,
            ReturnConsumedCapacity='TOTAL',
            Limit=20
        )
        
        execution_time = (time.time() - start_time) * 1000
        print(f"Second scan executed in {execution_time:.2f} ms")
        print(f"Additional items retrieved: {len(response2['Items'])}")
        print(f"Consumed capacity: {response2['ConsumedCapacity']['CapacityUnits']} RCUs")
        
        # Check if we have even more items
        if 'LastEvaluatedKey' in response2:
            print("\nMore items available. Scan can be continued.")
        else:
            print("\nNo more items to retrieve.")
            
        # Show sample items from second scan
        print("\n=== Sample Items from Second Scan ===")
        for item in response2['Items'][:3]:  # Show first 3 items
            print(json.dumps(item, indent=2, cls=DecimalEncoder))
    else:
        print("\nNo continuation token available (all data retrieved in first scan)")
    
    print("\n=== Starting Token Usage ===")
    print("Use starting tokens to implement pagination in your application")
    print("Store the LastEvaluatedKey between requests to continue where you left off")
    print("This is useful for implementing 'Next Page' functionality or for processing large datasets")

if __name__ == "__main__":
    scan_with_starting_token()
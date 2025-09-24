import sys
import os
import time
import json
from decimal import Decimal
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.dynamodb_helper import get_dynamodb_resource

class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert Decimal to float for JSON serialization."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def run_sequential_scan(table_name):
    """Perform a standard sequential scan of the entire table."""
    
    print("=== Running Sequential Scan ===")
    
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(table_name)
    
    # Start timing
    start_time = time.time()
    
    # Variables to track progress
    all_items = []
    total_scanned = 0
    consumed_capacity = 0
    
    # Initial scan
    response = table.scan(ReturnConsumedCapacity='TOTAL')
    
    # Process items
    all_items.extend(response['Items'])
    total_scanned += response['ScannedCount']
    consumed_capacity += response['ConsumedCapacity']['CapacityUnits']
    
    # Continue scanning if we have more items
    while 'LastEvaluatedKey' in response:
        print(f"Continuing scan... Items so far: {len(all_items)}")
        
        response = table.scan(
            ExclusiveStartKey=response['LastEvaluatedKey'],
            ReturnConsumedCapacity='TOTAL'
        )
        
        all_items.extend(response['Items'])
        total_scanned += response['ScannedCount']
        consumed_capacity += response['ConsumedCapacity']['CapacityUnits']
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    # Print results
    print("\n=== Sequential Scan Results ===")
    print(f"Total items retrieved: {len(all_items)}")
    print(f"Total items scanned: {total_scanned}")
    print(f"Total execution time: {execution_time:.2f} seconds")
    print(f"Items per second: {len(all_items) / execution_time:.2f}")
    print(f"Total consumed capacity: {consumed_capacity:.2f} RCUs")
    
    return {
        'items_count': len(all_items),
        'execution_time': execution_time,
        'items_per_second': len(all_items) / execution_time,
        'consumed_capacity': consumed_capacity
    }

if __name__ == "__main__":
    table_name = 'GameLeaderboard'
    result = run_sequential_scan(table_name)
    
    # Save result for comparison with parallel scan
    with open('sequential_scan_result.json', 'w') as f:
        json.dump(result, f, cls=DecimalEncoder, indent=2)
import boto3
import json
import time
from decimal import Decimal
from boto3.dynamodb.conditions import Key

class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert Decimal to float for JSON serialization."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def query_by_player_primary_key(player_id):
    """Query games by player ID using the primary key."""
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    print(f"\n=== Querying games for player {player_id} using PRIMARY KEY ===")
    
    # Start timing
    start_time = time.time()
    
    # Query using primary key
    response = table.query(
        KeyConditionExpression=Key('player_id').eq(player_id),
        ReturnConsumedCapacity='TOTAL'
    )
    
    # Calculate execution time
    execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    # Print results
    print(f"Query executed in {execution_time:.2f} ms")
    print(f"Items found: {len(response['Items'])}")
    print(f"Consumed capacity: {response['ConsumedCapacity']['CapacityUnits']} RCUs")
    
    return {
        'execution_time': execution_time,
        'items_count': len(response['Items']),
        'consumed_capacity': response['ConsumedCapacity']['CapacityUnits']
    }

def query_by_player_scan(player_id):
    """Query games by player ID using a scan operation (inefficient)."""
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    print(f"\n=== Querying games for player {player_id} using SCAN with filter ===")
    
    # Start timing
    start_time = time.time()
    
    # Scan with filter expression
    response = table.scan(
        FilterExpression=Key('player_id').eq(player_id),
        ReturnConsumedCapacity='TOTAL'
    )
    
    # Calculate execution time
    execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    # Print results
    print(f"Scan executed in {execution_time:.2f} ms")
    print(f"Items found: {len(response['Items'])}")
    print(f"Consumed capacity: {response['ConsumedCapacity']['CapacityUnits']} RCUs")
    
    return {
        'execution_time': execution_time,
        'items_count': len(response['Items']),
        'consumed_capacity': response['ConsumedCapacity']['CapacityUnits']
    }

def compare_performance():
    """Compare performance between primary key query and scan."""
    
    # Get a random player ID from the table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    # Get a sample player_id from the table
    response = table.scan(Limit=1)
    if len(response['Items']) == 0:
        print("No items found in the table. Please load data first.")
        return
    
    player_id = response['Items'][0]['player_id']
    
    # Run both query methods
    pk_results = query_by_player_primary_key(player_id)
    scan_results = query_by_player_scan(player_id)
    
    # Compare results
    time_diff = scan_results['execution_time'] / pk_results['execution_time']
    capacity_diff = scan_results['consumed_capacity'] / pk_results['consumed_capacity']
    
    print("\n=== Performance Comparison ===")
    print(f"Primary Key Query: {pk_results['execution_time']:.2f} ms, {pk_results['consumed_capacity']} RCUs")
    print(f"Scan with Filter: {scan_results['execution_time']:.2f} ms, {scan_results['consumed_capacity']} RCUs")
    print(f"Scan is {time_diff:.2f}x slower than Primary Key Query")
    print(f"Scan consumes {capacity_diff:.2f}x more capacity than Primary Key Query")
    
    print("\n=== Conclusion ===")
    print("Using the correct access pattern (Primary Key Query) for finding a player's games")
    print("is significantly faster and more cost-effective than using a scan operation.")

if __name__ == "__main__":
    compare_performance()
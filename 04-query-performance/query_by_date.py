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

def query_by_date_scan(game_date):
    """Query games by date using a scan operation (inefficient)."""
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    print(f"\n=== Querying games for date {game_date} using SCAN with filter ===")
    
    # Start timing
    start_time = time.time()
    
    # Scan with filter expression
    response = table.scan(
        FilterExpression=Key('game_date').eq(game_date),
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

def query_by_date_gsi(game_date):
    """Query games by date using the GSI (efficient)."""
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    print(f"\n=== Querying games for date {game_date} using GSI ===")
    
    # Start timing
    start_time = time.time()
    
    # Query using GSI
    response = table.query(
        IndexName='GameDateIndex',
        KeyConditionExpression=Key('game_date').eq(game_date),
        ReturnConsumedCapacity='TOTAL'
    )
    
    # Calculate execution time
    execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    # Print results
    print(f"GSI Query executed in {execution_time:.2f} ms")
    print(f"Items found: {len(response['Items'])}")
    print(f"Consumed capacity: {response['ConsumedCapacity']['CapacityUnits']} RCUs")
    
    return {
        'execution_time': execution_time,
        'items_count': len(response['Items']),
        'consumed_capacity': response['ConsumedCapacity']['CapacityUnits']
    }

def compare_performance():
    """Compare performance between GSI query and scan for date-based queries."""
    
    # Get a random date from the table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    # Get a sample game_date from the table
    response = table.scan(Limit=1)
    if len(response['Items']) == 0:
        print("No items found in the table. Please load data first.")
        return
    
    game_date = response['Items'][0]['game_date']
    
    # Run both query methods
    scan_results = query_by_date_scan(game_date)
    gsi_results = query_by_date_gsi(game_date)
    
    # Compare results
    time_diff = scan_results['execution_time'] / gsi_results['execution_time']
    capacity_diff = scan_results['consumed_capacity'] / gsi_results['consumed_capacity']
    
    print("\n=== Performance Comparison ===")
    print(f"GSI Query: {gsi_results['execution_time']:.2f} ms, {gsi_results['consumed_capacity']} RCUs")
    print(f"Scan with Filter: {scan_results['execution_time']:.2f} ms, {scan_results['consumed_capacity']} RCUs")
    print(f"Scan is {time_diff:.2f}x slower than GSI Query")
    print(f"Scan consumes {capacity_diff:.2f}x more capacity than GSI Query")
    
    print("\n=== Conclusion ===")
    print("Using the correct access pattern (GSI Query) for finding games by date")
    print("is significantly faster and more cost-effective than using a scan operation.")
    print("This demonstrates the importance of designing your table and indexes")
    print("based on your application's access patterns.")

if __name__ == "__main__":
    compare_performance()
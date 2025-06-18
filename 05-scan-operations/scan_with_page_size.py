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

def scan_with_page_size():
    """Demonstrate scan with pagination using a small page size."""
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    print("=== Scan with Page Size ===")
    print("Using a small page size (10) to demonstrate pagination")
    
    # Track API calls and timing
    api_calls = 0
    total_items = 0
    start_time = time.time()
    
    # Scan with small page size to demonstrate multiple API calls
    response = table.scan(
        ReturnConsumedCapacity='TOTAL',
        Limit=10  # Small page size to force multiple API calls
    )
    
    api_calls += 1
    total_items += len(response['Items'])
    print(f"\nAPI call {api_calls}: Retrieved {len(response['Items'])} items")
    
    # Continue scanning if we have more items
    while 'LastEvaluatedKey' in response:
        print(f"LastEvaluatedKey found: {json.dumps(response['LastEvaluatedKey'], cls=DecimalEncoder)}")
        
        response = table.scan(
            ExclusiveStartKey=response['LastEvaluatedKey'],
            ReturnConsumedCapacity='TOTAL',
            Limit=10
        )
        
        api_calls += 1
        total_items += len(response['Items'])
        print(f"API call {api_calls}: Retrieved {len(response['Items'])} items")
    
    # Calculate execution time
    execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    print(f"\nTotal execution time: {execution_time:.2f} ms")
    print(f"Total API calls: {api_calls}")
    print(f"Total items retrieved: {total_items}")
    
    print("\n=== Pagination Analysis ===")
    print("Pagination allows you to control memory usage and response size.")
    print("Each API call incurs latency, so balance page size with your application needs.")
    print("For batch processing, larger page sizes are more efficient.")
    print("For interactive applications, smaller page sizes provide better responsiveness.")

if __name__ == "__main__":
    scan_with_page_size()
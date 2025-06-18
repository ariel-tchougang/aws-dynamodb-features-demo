import boto3
import json
import time
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr

class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert Decimal to float for JSON serialization."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def scan_with_filter():
    """Demonstrate scan with filter expression and analyze filter efficiency."""
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    print("=== Scan with Filter Expression ===")
    print("Filtering for games with score > 9000")
    
    # Start timing
    start_time = time.time()
    
    # Scan with filter expression
    response = table.scan(
        FilterExpression=Attr('score').gt(9000),
        ReturnConsumedCapacity='TOTAL'
    )
    
    # Calculate execution time
    execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    # Print results
    print(f"\nScan executed in {execution_time:.2f} ms")
    print(f"Items scanned: {response['ScannedCount']}")
    print(f"Items matching filter: {len(response['Items'])}")
    print(f"Consumed capacity: {response['ConsumedCapacity']['CapacityUnits']} RCUs")
    
    # Calculate filter efficiency
    filter_efficiency = len(response['Items']) / response['ScannedCount'] * 100 if response['ScannedCount'] > 0 else 0
    print(f"\nFilter efficiency: {filter_efficiency:.2f}%")
    
    # Show the distribution of results across pages
    items_per_page = 100  # Assuming default page size
    estimated_pages = (response['ScannedCount'] + items_per_page - 1) // items_per_page
    avg_matches_per_page = len(response['Items']) / estimated_pages if estimated_pages > 0 else 0
    
    print("\n=== Filter Expression Analysis ===")
    print("Filter expressions are applied AFTER items are read from the table.")
    print("You are charged for reading ALL items, even if they don't match the filter.")
    print(f"Estimated number of pages: {estimated_pages}")
    print(f"Average matches per page: {avg_matches_per_page:.2f}")
    
    print("\n=== Sample Matching Items ===")
    for item in response['Items'][:3]:  # Show first 3 matching items
        print(json.dumps(item, indent=2, cls=DecimalEncoder))
    
    print("\n=== Recommendation ===")
    if filter_efficiency < 10:
        print("Low filter efficiency detected!")
        print("Consider using a Global Secondary Index (GSI) if you frequently filter on this attribute.")
    else:
        print("Filter efficiency is reasonable for this query pattern.")

if __name__ == "__main__":
    scan_with_filter()
import boto3
import time
import json
from decimal import Decimal
from botocore.config import Config
from botocore.exceptions import ClientError

class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert Decimal to float for JSON serialization."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def run_without_retry():
    """Run multiple get_item operations without retry configuration."""
    
    # Configure with no retries
    no_retry_config = Config(
        retries={
            'max_attempts': 0  # Disable retries
        }
    )
    
    dynamodb = boto3.resource('dynamodb', config=no_retry_config)
    table = dynamodb.Table('GameLeaderboard')
    
    print("=== Running Get Item Operations without Retry Configuration ===")
    print("Retry Config: max_attempts=0 (retries disabled)")
    
    # First, get some sample keys from the table
    try:
        response = table.scan(Limit=300, ProjectionExpression="player_id, game_id")
        items = response.get('Items', [])
    except ClientError as e:
        print(f"Error scanning table: {e}")
        return
    
    if not items:
        print("No items found in table. Please load data first.")
        return
    
    # Run multiple get_item operations in quick succession
    print(f"Performing {len(items) * 3} get_item operations (likely to trigger throttling)...")
    
    successful_requests = 0
    failed_requests = 0
    start_time = time.time()
    
    # Run each get_item operation 3 times to increase load
    for _ in range(3):
        for item in items:
            key = {
                'player_id': item['player_id'],
                'game_id': item['game_id']
            }
            
            try:
                # Get item without retry logic
                response = table.get_item(Key=key)
                successful_requests += 1
                
                # Small delay between requests to show progression
                time.sleep(0.05)
                
            except ClientError as e:
                if e.response['Error']['Code'] == 'ProvisionedThroughputExceededException':
                    print(f"Request throttled: {e.response['Error']['Message']}")
                    failed_requests += 1
                else:
                    print(f"Error: {e}")
                    failed_requests += 1
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    print("\n=== Results without Retry Configuration ===")
    print(f"Total requests: {len(items) * 3}")
    print(f"Successful requests: {successful_requests}")
    print(f"Failed requests: {failed_requests}")
    print(f"Total execution time: {execution_time:.2f} seconds")
    
    if failed_requests > 0:
        print("\n⚠️ Some requests failed due to throttling.")
        print("This demonstrates why retry configuration is important when working with DynamoDB.")
    else:
        print("\n✅ All requests succeeded without throttling.")
        print("Try increasing the number of concurrent requests to trigger throttling.")

if __name__ == "__main__":
    run_without_retry()
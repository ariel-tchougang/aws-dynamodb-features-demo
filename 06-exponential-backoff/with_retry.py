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

def run_with_retry():
    """Run multiple get_item operations with SDK's built-in retry configuration."""
    
    # Configure retry strategy
    retry_config = Config(
        retries={
            'max_attempts': 10,
            'mode': 'standard'  # Uses exponential backoff with jitter
        }
    )
    
    # Initialize DynamoDB with retry configuration
    dynamodb = boto3.resource('dynamodb', config=retry_config)
    table = dynamodb.Table('GameLeaderboard')
    
    print("=== Running Get Item Operations with SDK Retry Configuration ===")
    print("Retry Config: max_attempts=10, mode=standard (exponential backoff with jitter)")
    
    # First, get some sample keys from the table
    try:
        response = table.scan(Limit=10, ProjectionExpression="player_id, game_id")
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
    
    # Set up retry event listener to count retries
    total_retries = 0
    
    def count_retries(attempts, **kwargs):
        nonlocal total_retries
        if attempts > 0:
            total_retries += 1
            print(f"Request throttled. Retry attempt {attempts}")
    
    # Register the retry event listener
    dynamodb.meta.client.meta.events.register('after-retry.dynamodb', count_retries)
    
    # Run each get_item operation 3 times to increase load
    for _ in range(3):
        for item in items:
            key = {
                'player_id': item['player_id'],
                'game_id': item['game_id']
            }
            
            try:
                # Get item with SDK's built-in retry logic
                response = table.get_item(Key=key)
                successful_requests += 1
                
                # Small delay between requests to show progression
                time.sleep(0.05)
                
            except ClientError as e:
                print(f"Failed after all retries: {e}")
                failed_requests += 1
    
    # Unregister the event listener
    dynamodb.meta.client.meta.events.unregister('after-retry.dynamodb', count_retries)
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    print("\n=== Results with SDK Retry Configuration ===")
    print(f"Total requests: {len(items) * 3}")
    print(f"Successful requests: {successful_requests}")
    print(f"Failed requests: {failed_requests}")
    print(f"Total retries needed: {total_retries}")
    print(f"Total execution time: {execution_time:.2f} seconds")
    
    if successful_requests == len(items) * 3:
        print("\n✅ All requests eventually succeeded with retry logic!")
        print("This demonstrates how AWS SDK's built-in exponential backoff helps handle throttling.")
    else:
        print(f"\n⚠️ {failed_requests} requests failed even with retry logic.")

if __name__ == "__main__":
    run_with_retry()
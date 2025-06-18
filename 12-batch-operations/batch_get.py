import boto3
import time
import json
from decimal import Decimal
from botocore.exceptions import ClientError

class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert Decimal to float for JSON serialization."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def get_sample_keys(count=10):
    """Get sample keys from the table for batch operations."""
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    # Scan to get some sample keys
    response = table.scan(
        Limit=count,
        ProjectionExpression="player_id, game_id"
    )
    
    items = response.get('Items', [])
    
    if not items:
        print("No items found in table. Please load data first.")
        return []
    
    # Extract keys
    keys = [{'player_id': item['player_id'], 'game_id': item['game_id']} for item in items]
    
    return keys

def batch_get_with_retry(keys):
    """Retrieve multiple items using BatchGetItem with retry for unprocessed keys."""
    
    dynamodb = boto3.resource('dynamodb')
    
    # Start timing
    start_time = time.time()
    
    # Prepare keys for batch get
    keys_to_get = keys.copy()
    total_keys = len(keys_to_get)
    items_retrieved = []
    retries = 0
    
    print(f"Retrieving {total_keys} items using BatchGetItem...")
    
    while keys_to_get:
        try:
            # Perform batch get
            response = dynamodb.batch_get_item(
                RequestItems={
                    'GameLeaderboard': {
                        'Keys': keys_to_get
                    }
                },
                ReturnConsumedCapacity='TOTAL'
            )
            
            # Process retrieved items
            if 'GameLeaderboard' in response['Responses']:
                items_retrieved.extend(response['Responses']['GameLeaderboard'])
            
            # Handle unprocessed keys
            unprocessed = response.get('UnprocessedKeys', {}).get('GameLeaderboard', {}).get('Keys', [])
            if unprocessed:
                retries += 1
                print(f"Got {len(unprocessed)} unprocessed keys, retrying...")
                
                # Update keys to get
                keys_to_get = unprocessed
                
                # Exponential backoff
                time.sleep(min(0.1 * (2 ** retries), 1.0))
            else:
                # All keys processed
                keys_to_get = []
            
            # Print consumed capacity
            if 'ConsumedCapacity' in response:
                for capacity in response['ConsumedCapacity']:
                    print(f"Consumed capacity: {capacity['CapacityUnits']} RCUs")
            
        except ClientError as e:
            print(f"Error: {e.response['Error']['Message']}")
            retries += 1
            time.sleep(min(0.1 * (2 ** retries), 1.0))
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    print(f"\nBatch get completed:")
    print(f"- {len(items_retrieved)} items retrieved")
    print(f"- {retries} retries needed")
    print(f"- {execution_time:.2f} seconds total")
    
    return items_retrieved, execution_time

def individual_gets(keys):
    """Retrieve items individually for comparison."""
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    # Start timing
    start_time = time.time()
    
    total_keys = len(keys)
    items_retrieved = []
    
    print(f"\nRetrieving {total_keys} items individually...")
    
    for key in keys:
        response = table.get_item(Key=key)
        if 'Item' in response:
            items_retrieved.append(response['Item'])
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    print(f"\nIndividual gets completed:")
    print(f"- {len(items_retrieved)} items retrieved")
    print(f"- {execution_time:.2f} seconds total")
    
    return items_retrieved, execution_time

def compare_batch_vs_individual():
    """Compare batch gets vs individual gets."""
    
    # Get sample keys
    print("Getting sample keys...")
    keys = get_sample_keys(20)
    
    if not keys:
        return
    
    # Perform batch gets
    print("\n=== Batch Get Test ===")
    batch_items, batch_time = batch_get_with_retry(keys)
    
    # Perform individual gets
    print("\n=== Individual Get Test ===")
    individual_items, individual_time = individual_gets(keys)
    
    # Compare results
    speedup = individual_time / batch_time if batch_time > 0 else 0
    
    print("\n=== Performance Comparison ===")
    print(f"Batch get time: {batch_time:.2f} seconds")
    print(f"Individual get time: {individual_time:.2f} seconds")
    print(f"Batch gets are {speedup:.2f}x faster")
    
    # Show sample of retrieved items
    if batch_items:
        print("\n=== Sample Retrieved Item ===")
        print(json.dumps(batch_items[0], indent=2, cls=DecimalEncoder))

if __name__ == "__main__":
    print("=== DynamoDB BatchGetItem Demo ===")
    compare_batch_vs_individual()
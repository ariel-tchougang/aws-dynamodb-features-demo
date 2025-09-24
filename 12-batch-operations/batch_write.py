import sys
import os
import time
import uuid
import random
from decimal import Decimal
from botocore.exceptions import ClientError
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.dynamodb_helper import get_dynamodb_resource

def generate_game_records(count):
    """Generate multiple game records for batch writing."""
    
    game_modes = ["battle-royale", "team-deathmatch", "capture-the-flag", "survival"]
    achievements = ["FirstBlood", "DoubleKill", "TripleKill", "Headshot", "Survivor"]
    
    records = []
    
    for i in range(count):
        player_id = f"batch-p{uuid.uuid4().hex[:8]}"
        game_id = f"batch-g{uuid.uuid4().hex[:8]}"
        
        record = {
            'player_id': player_id,
            'game_id': game_id,
            'player_name': f"BatchPlayer{i}",
            'game_date': time.strftime("%Y-%m-%d"),
            'score': Decimal(str(random.randint(1000, 10000))),
            'game_duration': Decimal(str(random.randint(180, 900))),
            'achievements': random.sample(achievements, k=random.randint(0, 3)),
            'game_mode': random.choice(game_modes),
            'expiration_time': Decimal('0'),
            'last_updated': time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        
        records.append(record)
    
    return records

def batch_write_with_retry(records):
    """Write records in batches with retry for unprocessed items."""
    
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table('GameLeaderboard')
    
    # Start timing
    start_time = time.time()
    
    # Prepare items for batch write
    items_to_write = records.copy()
    batch_size = 25  # Maximum batch size for BatchWriteItem
    total_items = len(items_to_write)
    items_processed = 0
    retries = 0
    
    print(f"Writing {total_items} items in batches of {batch_size}...")
    
    while items_to_write:
        # Take up to batch_size items
        batch_items = items_to_write[:batch_size]
        items_to_write = items_to_write[batch_size:]
        
        # Prepare batch request
        batch_request = {
            table.name: [
                {
                    'PutRequest': {
                        'Item': item
                    }
                }
                for item in batch_items
            ]
        }
        
        try:
            # Perform batch write
            response = dynamodb.batch_write_item(
                RequestItems=batch_request,
                ReturnConsumedCapacity='TOTAL'
            )
            
            # Handle unprocessed items
            unprocessed = response.get('UnprocessedItems', {}).get(table.name, [])
            if unprocessed:
                retries += 1
                print(f"Got {len(unprocessed)} unprocessed items, retrying...")
                
                # Add unprocessed items back to the queue
                unprocessed_items = [item['PutRequest']['Item'] for item in unprocessed]
                items_to_write = unprocessed_items + items_to_write
                
                # Exponential backoff
                time.sleep(min(0.1 * (2 ** retries), 1.0))
            
            # Update progress
            items_processed += len(batch_items) - len(unprocessed)
            print(f"Progress: {items_processed}/{total_items} items processed")
            
        except ClientError as e:
            print(f"Error: {e.response['Error']['Message']}")
            # Add items back to the queue
            items_to_write = batch_items + items_to_write
            retries += 1
            time.sleep(min(0.1 * (2 ** retries), 1.0))
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    print(f"\nBatch write completed:")
    print(f"- {total_items} items written")
    print(f"- {retries} retries needed")
    print(f"- {execution_time:.2f} seconds total")
    print(f"- {total_items / execution_time:.2f} items/second")
    
    return execution_time

def individual_writes(records):
    """Write records individually for comparison."""
    
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table('GameLeaderboard')
    
    # Start timing
    start_time = time.time()
    
    total_items = len(records)
    
    print(f"\nWriting {total_items} items individually...")
    
    for i, item in enumerate(records):
        table.put_item(Item=item)
        
        # Update progress every 10 items
        if (i + 1) % 10 == 0:
            print(f"Progress: {i + 1}/{total_items} items processed")
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    print(f"\nIndividual writes completed:")
    print(f"- {total_items} items written")
    print(f"- {execution_time:.2f} seconds total")
    print(f"- {total_items / execution_time:.2f} items/second")
    
    return execution_time

def compare_batch_vs_individual():
    """Compare batch writes vs individual writes."""
    
    # Generate test data - 50 records
    print("Generating test data...")
    records = generate_game_records(50)
    
    # Perform batch writes
    print("\n=== Batch Write Test ===")
    batch_time = batch_write_with_retry(records)
    
    # Generate new set of records for individual writes
    records = generate_game_records(50)
    
    # Perform individual writes
    print("\n=== Individual Write Test ===")
    individual_time = individual_writes(records)
    
    # Compare results
    speedup = individual_time / batch_time if batch_time > 0 else 0
    
    print("\n=== Performance Comparison ===")
    print(f"Batch write time: {batch_time:.2f} seconds")
    print(f"Individual write time: {individual_time:.2f} seconds")
    print(f"Batch writes are {speedup:.2f}x faster")

if __name__ == "__main__":
    print("=== DynamoDB BatchWriteItem Demo ===")
    compare_batch_vs_individual()
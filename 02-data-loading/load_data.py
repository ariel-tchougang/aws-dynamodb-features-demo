import json
import sys
import os
import time
from decimal import Decimal
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.dynamodb_helper import get_dynamodb_resource

def load_data_to_dynamodb(filename="game_data.json"):
    """Load game data from JSON file to DynamoDB table."""
    
    # Read the JSON file
    with open(filename, 'r') as f:
        game_data = json.load(f)
    
    # Convert to DynamoDB format (Decimal for numbers)
    for item in game_data:
        item['score'] = Decimal(str(item['score']))
        item['game_duration'] = Decimal(str(item['game_duration']))
        item['expiration_time'] = Decimal(str(item['expiration_time']))
    
    # Initialize DynamoDB resource
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table('GameLeaderboard')
    
    # Track progress
    total_items = len(game_data)
    loaded_items = 0
    start_time = time.time()
    
    print(f"Starting to load {total_items} items into DynamoDB...")
    
    # Use batch_writer to efficiently load items
    with table.batch_writer() as batch:
        for item in game_data:
            batch.put_item(Item=item)
            loaded_items += 1
            
            # Print progress every 100 items
            if loaded_items % 100 == 0:
                elapsed_time = time.time() - start_time
                items_per_second = loaded_items / elapsed_time if elapsed_time > 0 else 0
                print(f"Loaded {loaded_items}/{total_items} items ({items_per_second:.2f} items/second)")
    
    # Final stats
    total_time = time.time() - start_time
    final_rate = total_items / total_time if total_time > 0 else 0
    
    print(f"\nData loading complete!")
    print(f"Loaded {total_items} items in {total_time:.2f} seconds")
    print(f"Average rate: {final_rate:.2f} items/second")

if __name__ == "__main__":
    load_data_to_dynamodb()
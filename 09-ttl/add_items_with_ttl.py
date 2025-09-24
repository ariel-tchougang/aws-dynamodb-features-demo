import sys
import os
import time
import uuid
import random
from decimal import Decimal
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.dynamodb_helper import get_dynamodb_resource

def add_items_with_ttl():
    """Add items with various TTL expiration times."""
    
    # Initialize DynamoDB resource
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table('GameLeaderboard')
    
    # Current time in epoch seconds
    current_time = int(time.time())
    
    # Define expiration times
    expiration_times = {
        '2 minutes': current_time + 120,
        '5 minutes': current_time + 300,
        '10 minutes': current_time + 600,
        'No expiration': 0  # 0 means no expiration
    }
    
    # Game modes for our test data
    game_modes = ['seasonal-event', 'regular-match', 'tournament']
    
    print("Adding items with different TTL values...")
    
    # Add 5 items for each expiration time
    for expiration_name, expiration_time in expiration_times.items():
        print(f"\nAdding items that expire in: {expiration_name}")
        
        for i in range(5):
            # Generate unique IDs
            player_id = f"ttl-p{uuid.uuid4().hex[:8]}"
            game_id = f"ttl-g{uuid.uuid4().hex[:8]}"
            
            # Create item with TTL
            item = {
                'player_id': player_id,
                'game_id': game_id,
                'player_name': f"TTLPlayer{i}",
                'game_date': time.strftime("%Y-%m-%d"),
                'score': Decimal(str(random.randint(1000, 10000))),
                'game_duration': Decimal(str(random.randint(180, 900))),
                'achievements': random.sample(['FirstBlood', 'DoubleKill', 'TripleKill'], 
                                           k=random.randint(0, 3)),
                'game_mode': random.choice(game_modes),
                'expiration_time': Decimal(str(expiration_time)),
                'last_updated': time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
            
            # Add item to table
            table.put_item(Item=item)
            
            # Print item details
            expiry_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expiration_time)) if expiration_time > 0 else 'Never'
            print(f"  Added: {player_id} / {game_id} - Expires: {expiry_str}")
    
    print("\nAll items added successfully!")
    print("\nNOTE: TTL deletion typically occurs within 48 hours of expiration.")
    print("      For this lab, we'll check periodically to observe the deletions.")

if __name__ == "__main__":
    add_items_with_ttl()
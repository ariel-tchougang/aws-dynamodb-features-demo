import boto3
import time
import random
import uuid
import threading
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor

def generate_game_record():
    """Generate a random game record."""
    player_id = f"p{uuid.uuid4().hex[:8]}"
    game_id = f"g{uuid.uuid4().hex[:8]}"
    
    return {
        'player_id': player_id,
        'game_id': game_id,
        'player_name': f"Player{random.randint(1, 999)}",
        'game_date': time.strftime("%Y-%m-%d"),
        'score': Decimal(str(random.randint(1000, 10000))),
        'game_duration': Decimal(str(random.randint(180, 900))),
        'achievements': random.sample(['FirstBlood', 'DoubleKill', 'TripleKill', 'Headshot', 'Survivor'], 
                                     k=random.randint(0, 3)),
        'game_mode': random.choice(['battle-royale', 'team-deathmatch', 'capture-the-flag']),
        'expiration_time': Decimal('0'),
        'last_updated': time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }

def write_items(dynamodb, count):
    """Write items to the table."""
    table = dynamodb.Table('GameLeaderboard')
    
    for _ in range(count):
        item = generate_game_record()
        table.put_item(Item=item)

def read_items(dynamodb, count):
    """Read random items from the table."""
    table = dynamodb.Table('GameLeaderboard')
    
    # Get some sample keys
    response = table.scan(Limit=min(count, 20), ProjectionExpression="player_id, game_id")
    items = response.get('Items', [])
    
    if not items:
        print("No items found in table. Cannot perform reads.")
        return
    
    # Perform reads
    for _ in range(count):
        item = random.choice(items)
        table.get_item(Key={
            'player_id': item['player_id'],
            'game_id': item['game_id']
        })

def generate_traffic():
    """Generate increasing traffic to trigger auto-scaling."""
    
    dynamodb = boto3.resource('dynamodb')
    
    print("Starting traffic generation to trigger auto-scaling...")
    print("Press Ctrl+C to stop")
    
    try:
        # Start with low traffic
        operations_per_second = 5
        
        while True:
            print(f"Generating {operations_per_second} operations per second...")
            
            # Use ThreadPoolExecutor to parallelize operations
            with ThreadPoolExecutor(max_workers=operations_per_second) as executor:
                # Mix of reads and writes
                read_count = int(operations_per_second * 0.7)  # 70% reads
                write_count = operations_per_second - read_count  # 30% writes
                
                # Submit tasks
                read_future = executor.submit(read_items, dynamodb, read_count)
                write_future = executor.submit(write_items, dynamodb, write_count)
                
                # Wait for completion
                read_future.result()
                write_future.result()
            
            # Increase traffic every 30 seconds
            if operations_per_second < 100:
                operations_per_second += 5
            
            # Wait before next batch
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nTraffic generation stopped.")

if __name__ == "__main__":
    generate_traffic()
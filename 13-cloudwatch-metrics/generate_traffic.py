import boto3
import time
import uuid
import random
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

def scan_items(dynamodb):
    """Perform scan operations."""
    table = dynamodb.Table('GameLeaderboard')
    table.scan(Limit=50)

def query_items(dynamodb):
    """Perform query operations."""
    table = dynamodb.Table('GameLeaderboard')
    
    # Get a sample player_id
    response = table.scan(Limit=1, ProjectionExpression="player_id")
    items = response.get('Items', [])
    
    if not items:
        print("No items found in table. Cannot perform query.")
        return
    
    player_id = items[0]['player_id']
    
    # Query by player_id
    table.query(
        KeyConditionExpression="player_id = :pid",
        ExpressionAttributeValues={
            ":pid": player_id
        }
    )

def generate_traffic():
    """Generate mixed traffic to produce various CloudWatch metrics."""
    
    dynamodb = boto3.resource('dynamodb')
    
    print("Starting traffic generation for CloudWatch metrics...")
    print("This will run for 5 minutes. Press Ctrl+C to stop early.")
    
    try:
        # Run for 5 minutes
        end_time = time.time() + 300  # 5 minutes
        
        while time.time() < end_time:
            # Mix of operations
            operations = [
                # Operation type, weight
                ("read", 50),    # 50% reads
                ("write", 30),   # 30% writes
                ("scan", 10),    # 10% scans
                ("query", 10)    # 10% queries
            ]
            
            # Select operation based on weights
            op_types, weights = zip(*operations)
            operation = random.choices(op_types, weights=weights, k=1)[0]
            
            # Perform selected operation
            if operation == "read":
                read_items(dynamodb, random.randint(5, 15))
            elif operation == "write":
                write_items(dynamodb, random.randint(3, 8))
            elif operation == "scan":
                scan_items(dynamodb)
            elif operation == "query":
                query_items(dynamodb)
            
            # Short pause between operations
            time.sleep(0.5)
            
            # Print progress
            remaining = int(end_time - time.time())
            print(f"Generated {operation} traffic. {remaining} seconds remaining...", end="\r")
            
    except KeyboardInterrupt:
        print("\nTraffic generation stopped.")
    
    print("\nTraffic generation complete. CloudWatch metrics should now be available.")
    print("Run 'python view_metrics.py' to see the metrics.")

if __name__ == "__main__":
    print("=== Generating Traffic for CloudWatch Metrics ===")
    generate_traffic()
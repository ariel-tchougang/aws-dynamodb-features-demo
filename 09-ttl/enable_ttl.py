import boto3
import time

def enable_ttl():
    """Enable Time to Live (TTL) on the GameLeaderboard table."""
    
    # Initialize DynamoDB client
    dynamodb = boto3.client('dynamodb')
    table_name = 'GameLeaderboard'
    
    print(f"Enabling TTL on table: {table_name}")
    
    # Check current TTL status
    ttl_status = dynamodb.describe_time_to_live(TableName=table_name)
    
    if 'TimeToLiveDescription' in ttl_status and ttl_status['TimeToLiveDescription'].get('TimeToLiveStatus') == 'ENABLED':
        print(f"TTL is already enabled on {table_name} with attribute: {ttl_status['TimeToLiveDescription'].get('AttributeName')}")
        return
    
    # Enable TTL
    response = dynamodb.update_time_to_live(
        TableName=table_name,
        TimeToLiveSpecification={
            'Enabled': True,
            'AttributeName': 'expiration_time'
        }
    )
    
    print(f"TTL enabled on {table_name} with attribute: expiration_time")
    print("Status:", response['TimeToLiveSpecification']['Enabled'])
    
    # Wait for TTL to be fully enabled
    print("Waiting for TTL to be fully enabled...")
    while True:
        ttl_status = dynamodb.describe_time_to_live(TableName=table_name)
        status = ttl_status['TimeToLiveDescription']['TimeToLiveStatus']
        
        if status == 'ENABLED':
            print("TTL is now fully enabled!")
            break
        
        print(f"Current TTL status: {status}. Waiting...")
        time.sleep(5)

if __name__ == "__main__":
    enable_ttl()
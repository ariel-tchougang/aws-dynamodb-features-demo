import boto3
import time
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key, Attr

def monitor_ttl():
    """Monitor TTL deletions and metrics."""
    
    # Initialize clients
    dynamodb = boto3.resource('dynamodb')
    cloudwatch = boto3.client('cloudwatch')
    
    table = dynamodb.Table('GameLeaderboard')
    table_name = 'GameLeaderboard'
    
    # Current time in epoch seconds
    current_time = int(time.time())
    
    print(f"=== Monitoring TTL for table: {table_name} ===")
    print(f"Current time: {datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Count items by expiration status
    def count_items_by_expiration():
        # Count items that should be expired (TTL in the past)
        expired_response = table.scan(
            FilterExpression=Attr('expiration_time').gt(0) & Attr('expiration_time').lt(current_time),
            Select='COUNT'
        )
        
        # Count items expiring soon (within next 10 minutes)
        expiring_soon_response = table.scan(
            FilterExpression=Attr('expiration_time').gt(current_time) & 
                            Attr('expiration_time').lt(current_time + 600),
            Select='COUNT'
        )
        
        # Count items with TTL set but not expiring soon
        future_response = table.scan(
            FilterExpression=Attr('expiration_time').gt(current_time + 600),
            Select='COUNT'
        )
        
        # Count items with no TTL
        no_ttl_response = table.scan(
            FilterExpression=Attr('expiration_time').eq(0),
            Select='COUNT'
        )
        
        return {
            'expired': expired_response['Count'],
            'expiring_soon': expiring_soon_response['Count'],
            'future': future_response['Count'],
            'no_ttl': no_ttl_response['Count']
        }
    
    # Get TTL deletion metrics from CloudWatch
    def get_ttl_metrics():
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=1)
        
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/DynamoDB',
            MetricName='TimeToLiveDeletedItemCount',
            Dimensions=[{'Name': 'TableName', 'Value': table_name}],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,  # 5-minute periods
            Statistics=['Sum']
        )
        
        # Extract datapoints
        datapoints = response['Datapoints']
        datapoints.sort(key=lambda x: x['Timestamp'])
        
        return datapoints
    
    # Initial count
    print("\nInitial item counts:")
    counts = count_items_by_expiration()
    print(f"- Items that should be expired: {counts['expired']}")
    print(f"- Items expiring soon (next 10 min): {counts['expiring_soon']}")
    print(f"- Items with future TTL: {counts['future']}")
    print(f"- Items with no TTL: {counts['no_ttl']}")
    
    # Initial TTL metrics
    print("\nRecent TTL deletion metrics:")
    ttl_metrics = get_ttl_metrics()
    if ttl_metrics:
        for point in ttl_metrics[-3:]:  # Show last 3 datapoints
            timestamp = point['Timestamp'].strftime('%H:%M:%S')
            deleted_count = int(point['Sum'])
            print(f"- {timestamp}: {deleted_count} items deleted")
    else:
        print("No TTL deletions recorded in the last hour.")
    
    # Monitor loop
    print("\nStarting TTL monitoring. Press Ctrl+C to stop.")
    try:
        check_count = 1
        while True:
            time.sleep(60)  # Check every minute
            
            print(f"\n=== Check #{check_count} at {datetime.now().strftime('%H:%M:%S')} ===")
            
            # Update counts
            counts = count_items_by_expiration()
            print(f"- Items that should be expired: {counts['expired']}")
            print(f"- Items expiring soon (next 10 min): {counts['expiring_soon']}")
            
            # Update TTL metrics
            ttl_metrics = get_ttl_metrics()
            if ttl_metrics:
                latest = ttl_metrics[-1]
                timestamp = latest['Timestamp'].strftime('%H:%M:%S')
                deleted_count = int(latest['Sum'])
                print(f"- Latest TTL metric ({timestamp}): {deleted_count} items deleted")
            
            check_count += 1
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    monitor_ttl()
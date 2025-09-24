import sys
import os
import time
from datetime import datetime, timedelta
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.dynamodb_helper import get_dynamodb_client

def get_dynamodb_metrics():
    """Retrieve and display DynamoDB CloudWatch metrics."""
    
    # Initialize CloudWatch client
    import boto3
    cloudwatch = boto3.client('cloudwatch')
    
    # Table name
    table_name = 'GameLeaderboard'
    
    # Define time range for metrics (last 30 minutes)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=30)
    
    print(f"=== DynamoDB CloudWatch Metrics for {table_name} ===")
    print(f"Time range: {start_time.strftime('%H:%M:%S')} to {end_time.strftime('%H:%M:%S')} UTC")
    
    # Define metrics to retrieve
    metrics = [
        {
            'name': 'ConsumedReadCapacityUnits',
            'stat': 'Sum',
            'unit': 'Count',
            'description': 'Read capacity units consumed'
        },
        {
            'name': 'ConsumedWriteCapacityUnits',
            'stat': 'Sum',
            'unit': 'Count',
            'description': 'Write capacity units consumed'
        },
        {
            'name': 'ReadThrottleEvents',
            'stat': 'Sum',
            'unit': 'Count',
            'description': 'Throttled read requests'
        },
        {
            'name': 'WriteThrottleEvents',
            'stat': 'Sum',
            'unit': 'Count',
            'description': 'Throttled write requests'
        },
        {
            'name': 'SuccessfulRequestLatency',
            'stat': 'Average',
            'unit': 'Milliseconds',
            'description': 'Average request latency',
            'operation': 'GetItem'
        },
        {
            'name': 'SuccessfulRequestLatency',
            'stat': 'Average',
            'unit': 'Milliseconds',
            'description': 'Average request latency',
            'operation': 'PutItem'
        }
    ]
    
    # Retrieve and display each metric
    for metric in metrics:
        dimensions = [{'Name': 'TableName', 'Value': table_name}]
        
        # Add Operation dimension if specified
        if 'operation' in metric:
            dimensions.append({'Name': 'Operation', 'Value': metric['operation']})
            print(f"\n--- {metric['description']} ({metric['operation']}) ---")
        else:
            print(f"\n--- {metric['description']} ---")
        
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/DynamoDB',
            MetricName=metric['name'],
            Dimensions=dimensions,
            StartTime=start_time,
            EndTime=end_time,
            Period=60,  # 1-minute periods
            Statistics=[metric['stat']]
        )
        
        datapoints = response['Datapoints']
        
        if not datapoints:
            print("No data available for this metric in the specified time range.")
            continue
        
        # Sort datapoints by timestamp
        datapoints.sort(key=lambda x: x['Timestamp'])
        
        # Display the most recent datapoints
        print(f"Recent values ({metric['stat']}):")
        for point in datapoints[-5:]:  # Show last 5 datapoints
            timestamp = point['Timestamp'].strftime('%H:%M:%S')
            value = point[metric['stat']]
            print(f"  {timestamp}: {value:.2f} {metric['unit']}")
        
        # Calculate and display statistics
        if datapoints:
            values = [point[metric['stat']] for point in datapoints]
            max_value = max(values)
            avg_value = sum(values) / len(values)
            
            print(f"Maximum: {max_value:.2f} {metric['unit']}")
            print(f"Average: {avg_value:.2f} {metric['unit']}")
    
    print("\n=== Provisioned Capacity ===")
    
    # Get current provisioned capacity
    dynamodb = get_dynamodb_client()
    table_info = dynamodb.describe_table(TableName=table_name)['Table']
    
    read_capacity = table_info['ProvisionedThroughput']['ReadCapacityUnits']
    write_capacity = table_info['ProvisionedThroughput']['WriteCapacityUnits']
    
    print(f"Read Capacity Units: {read_capacity}")
    print(f"Write Capacity Units: {write_capacity}")
    
    # Check if auto-scaling is enabled
    try:
        import boto3
        application_autoscaling = boto3.client('application-autoscaling')
        
        read_scaling = application_autoscaling.describe_scalable_targets(
            ServiceNamespace='dynamodb',
            ResourceIds=[f'table/{table_name}'],
            ScalableDimension='dynamodb:table:ReadCapacityUnits'
        )
        
        write_scaling = application_autoscaling.describe_scalable_targets(
            ServiceNamespace='dynamodb',
            ResourceIds=[f'table/{table_name}'],
            ScalableDimension='dynamodb:table:WriteCapacityUnits'
        )
        
        if read_scaling['ScalableTargets']:
            min_capacity = read_scaling['ScalableTargets'][0]['MinCapacity']
            max_capacity = read_scaling['ScalableTargets'][0]['MaxCapacity']
            print(f"Read Auto-scaling: Enabled (Min: {min_capacity}, Max: {max_capacity})")
        
        if write_scaling['ScalableTargets']:
            min_capacity = write_scaling['ScalableTargets'][0]['MinCapacity']
            max_capacity = write_scaling['ScalableTargets'][0]['MaxCapacity']
            print(f"Write Auto-scaling: Enabled (Min: {min_capacity}, Max: {max_capacity})")
            
    except Exception as e:
        print(f"Could not retrieve auto-scaling information: {str(e)}")

if __name__ == "__main__":
    get_dynamodb_metrics()
import sys
import os
import time
from datetime import datetime, timedelta
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.dynamodb_helper import get_dynamodb_client

def monitor_autoscaling():
    """Monitor auto-scaling activities and metrics."""
    
    # Initialize clients
    dynamodb = get_dynamodb_client()
    import boto3
    cloudwatch = boto3.client('cloudwatch')
    application_autoscaling = boto3.client('application-autoscaling')
    
    table_name = 'GameLeaderboard'
    
    print(f"Monitoring auto-scaling for table: {table_name}")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            # Get current table capacity
            table = dynamodb.describe_table(TableName=table_name)['Table']
            read_capacity = table['ProvisionedThroughput']['ReadCapacityUnits']
            write_capacity = table['ProvisionedThroughput']['WriteCapacityUnits']
            
            # Get consumed capacity metrics
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=5)
            
            metrics = cloudwatch.get_metric_data(
                MetricDataQueries=[
                    {
                        'Id': 'readCapacity',
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'AWS/DynamoDB',
                                'MetricName': 'ConsumedReadCapacityUnits',
                                'Dimensions': [{'Name': 'TableName', 'Value': table_name}]
                            },
                            'Period': 60,
                            'Stat': 'Sum'
                        }
                    },
                    {
                        'Id': 'writeCapacity',
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'AWS/DynamoDB',
                                'MetricName': 'ConsumedWriteCapacityUnits',
                                'Dimensions': [{'Name': 'TableName', 'Value': table_name}]
                            },
                            'Period': 60,
                            'Stat': 'Sum'
                        }
                    }
                ],
                StartTime=start_time,
                EndTime=end_time
            )
            
            # Get recent scaling activities
            read_activities = application_autoscaling.describe_scaling_activities(
                ServiceNamespace='dynamodb',
                ResourceId=f'table/{table_name}',
                ScalableDimension='dynamodb:table:ReadCapacityUnits',
                MaxResults=5
            )
            
            write_activities = application_autoscaling.describe_scaling_activities(
                ServiceNamespace='dynamodb',
                ResourceId=f'table/{table_name}',
                ScalableDimension='dynamodb:table:WriteCapacityUnits',
                MaxResults=5
            )
            
            # Clear screen
            print("\033[H\033[J")
            
            # Print current status
            print(f"=== DynamoDB Auto-scaling Monitor ({datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}) ===")
            print(f"\nProvisioned Capacity:")
            print(f"- Read Capacity Units: {read_capacity}")
            print(f"- Write Capacity Units: {write_capacity}")
            
            print(f"\nRecent Consumed Capacity (last datapoint):")
            if metrics['MetricDataResults'][0]['Values']:
                print(f"- Read Capacity: {metrics['MetricDataResults'][0]['Values'][-1]:.2f} RCUs")
            if metrics['MetricDataResults'][1]['Values']:
                print(f"- Write Capacity: {metrics['MetricDataResults'][1]['Values'][-1]:.2f} WCUs")
            
            print("\nRecent Scaling Activities:")
            print("Read Capacity:")
            for activity in read_activities['ScalingActivities'][:3]:
                print(f"- {activity['StartTime'].strftime('%H:%M:%S')}: {activity['StatusMessage']}")
            
            print("\nWrite Capacity:")
            for activity in write_activities['ScalingActivities'][:3]:
                print(f"- {activity['StartTime'].strftime('%H:%M:%S')}: {activity['StatusMessage']}")
            
            # Wait before next update
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    monitor_autoscaling()
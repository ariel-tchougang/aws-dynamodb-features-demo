import boto3
import json

def create_dynamodb_alarms():
    """Create CloudWatch alarms for DynamoDB metrics."""
    
    # Initialize CloudWatch client
    cloudwatch = boto3.client('cloudwatch')
    
    # Table name
    table_name = 'GameLeaderboard'
    
    print(f"=== Creating CloudWatch Alarms for {table_name} ===")
    
    # Define alarms to create
    alarms = [
        {
            'name': f"{table_name}-HighReadCapacity",
            'description': 'Alarm when read capacity exceeds 80% of provisioned capacity',
            'metric_name': 'ConsumedReadCapacityUnits',
            'threshold': 4,  # 80% of 5 RCUs
            'comparison_operator': 'GreaterThanThreshold',
            'evaluation_periods': 5,
            'period': 60,
            'statistic': 'Sum',
            'treat_missing_data': 'notBreaching'
        },
        {
            'name': f"{table_name}-HighWriteCapacity",
            'description': 'Alarm when write capacity exceeds 80% of provisioned capacity',
            'metric_name': 'ConsumedWriteCapacityUnits',
            'threshold': 4,  # 80% of 5 WCUs
            'comparison_operator': 'GreaterThanThreshold',
            'evaluation_periods': 5,
            'period': 60,
            'statistic': 'Sum',
            'treat_missing_data': 'notBreaching'
        },
        {
            'name': f"{table_name}-ReadThrottles",
            'description': 'Alarm when read throttling occurs',
            'metric_name': 'ReadThrottleEvents',
            'threshold': 0,
            'comparison_operator': 'GreaterThanThreshold',
            'evaluation_periods': 1,
            'period': 60,
            'statistic': 'Sum',
            'treat_missing_data': 'notBreaching'
        },
        {
            'name': f"{table_name}-WriteThrottles",
            'description': 'Alarm when write throttling occurs',
            'metric_name': 'WriteThrottleEvents',
            'threshold': 0,
            'comparison_operator': 'GreaterThanThreshold',
            'evaluation_periods': 1,
            'period': 60,
            'statistic': 'Sum',
            'treat_missing_data': 'notBreaching'
        },
        {
            'name': f"{table_name}-HighLatency",
            'description': 'Alarm when request latency is high',
            'metric_name': 'SuccessfulRequestLatency',
            'threshold': 100,  # 100ms
            'comparison_operator': 'GreaterThanThreshold',
            'evaluation_periods': 3,
            'period': 60,
            'statistic': 'Average',
            'treat_missing_data': 'notBreaching',
            'dimensions': [
                {
                    'Name': 'TableName',
                    'Value': table_name
                },
                {
                    'Name': 'Operation',
                    'Value': 'GetItem'
                }
            ]
        }
    ]
    
    # Create each alarm
    for alarm in alarms:
        # Default dimensions
        dimensions = alarm.get('dimensions', [
            {
                'Name': 'TableName',
                'Value': table_name
            }
        ])
        
        try:
            response = cloudwatch.put_metric_alarm(
                AlarmName=alarm['name'],
                AlarmDescription=alarm['description'],
                ActionsEnabled=False,  # No actions for this demo
                MetricName=alarm['metric_name'],
                Namespace='AWS/DynamoDB',
                Statistic=alarm['statistic'],
                Dimensions=dimensions,
                Period=alarm['period'],
                EvaluationPeriods=alarm['evaluation_periods'],
                Threshold=alarm['threshold'],
                ComparisonOperator=alarm['comparison_operator'],
                TreatMissingData=alarm['treat_missing_data']
            )
            
            print(f"Created alarm: {alarm['name']}")
            print(f"  Description: {alarm['description']}")
            print(f"  Threshold: {alarm['threshold']} ({alarm['comparison_operator']})")
            print(f"  Evaluation: {alarm['evaluation_periods']} periods of {alarm['period']} seconds")
            print()
            
        except Exception as e:
            print(f"Error creating alarm {alarm['name']}: {str(e)}")
    
    print("\nAlarms created successfully!")
    print("You can view these alarms in the CloudWatch console.")
    print("Note: In a production environment, you would configure actions for these alarms.")

if __name__ == "__main__":
    create_dynamodb_alarms()
import boto3
import time

def configure_autoscaling():
    """Configure auto-scaling for the GameLeaderboard table."""
    
    # Initialize clients
    dynamodb = boto3.client('dynamodb')
    application_autoscaling = boto3.client('application-autoscaling')
    
    table_name = 'GameLeaderboard'
    
    print(f"Configuring auto-scaling for table: {table_name}")
    
    # Define scaling targets for read and write capacity
    read_target = f"table/{table_name}"
    write_target = f"table/{table_name}"
    
    # Register scalable targets
    print("Registering scalable targets...")
    
    # Register read capacity target
    application_autoscaling.register_scalable_target(
        ServiceNamespace='dynamodb',
        ResourceId=read_target,
        ScalableDimension='dynamodb:table:ReadCapacityUnits',
        MinCapacity=5,
        MaxCapacity=100
    )
    
    # Register write capacity target
    application_autoscaling.register_scalable_target(
        ServiceNamespace='dynamodb',
        ResourceId=write_target,
        ScalableDimension='dynamodb:table:WriteCapacityUnits',
        MinCapacity=5,
        MaxCapacity=100
    )
    
    print("Configuring scaling policies...")
    
    # Configure scaling policy for read capacity
    application_autoscaling.put_scaling_policy(
        ServiceNamespace='dynamodb',
        ResourceId=read_target,
        ScalableDimension='dynamodb:table:ReadCapacityUnits',
        PolicyName='ReadCapacityUtilization',
        PolicyType='TargetTrackingScaling',
        TargetTrackingScalingPolicyConfiguration={
            'TargetValue': 70.0,
            'PredefinedMetricSpecification': {
                'PredefinedMetricType': 'DynamoDBReadCapacityUtilization'
            },
            'ScaleOutCooldown': 60,
            'ScaleInCooldown': 60
        }
    )
    
    # Configure scaling policy for write capacity
    application_autoscaling.put_scaling_policy(
        ServiceNamespace='dynamodb',
        ResourceId=write_target,
        ScalableDimension='dynamodb:table:WriteCapacityUnits',
        PolicyName='WriteCapacityUtilization',
        PolicyType='TargetTrackingScaling',
        TargetTrackingScalingPolicyConfiguration={
            'TargetValue': 70.0,
            'PredefinedMetricSpecification': {
                'PredefinedMetricType': 'DynamoDBWriteCapacityUtilization'
            },
            'ScaleOutCooldown': 60,
            'ScaleInCooldown': 60
        }
    )
    
    print("Auto-scaling configuration complete!")
    print("- Target utilization: 70%")
    print("- Min capacity: 5 RCUs/WCUs")
    print("- Max capacity: 100 RCUs/WCUs")
    print("- Scale out cooldown: 60 seconds")
    print("- Scale in cooldown: 60 seconds")

if __name__ == "__main__":
    configure_autoscaling()
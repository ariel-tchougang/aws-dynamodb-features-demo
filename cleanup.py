import sys
import os
import time
sys.path.append(os.path.dirname(__file__))
from utils.dynamodb_helper import get_dynamodb_client
import boto3

def cleanup_dynamodb_tables():
    """Clean up DynamoDB tables."""
    print("=== Cleaning up DynamoDB Tables ===")
    
    dynamodb = get_dynamodb_client()
    tables_to_delete = ['GameLeaderboard', 'PlayerInventory', 'GameAchievements']
    
    for table_name in tables_to_delete:
        try:
            dynamodb.describe_table(TableName=table_name)
            print(f"Deleting table: {table_name}...")
            dynamodb.delete_table(TableName=table_name)
            
            waiter = dynamodb.get_waiter('table_not_exists')
            waiter.wait(TableName=table_name)
            print(f"Table {table_name} deleted successfully.")
        except dynamodb.exceptions.ResourceNotFoundException:
            print(f"Table {table_name} does not exist.")
        except Exception as e:
            print(f"Error deleting table {table_name}: {e}")
            return False
    return True

def cleanup_cloudwatch_alarms():
    """Clean up CloudWatch alarms created in Lab 13."""
    print("\n=== Cleaning up CloudWatch Alarms ===")
    
    cloudwatch = boto3.client('cloudwatch')
    table_name = 'GameLeaderboard'
    
    alarm_names = [
        f"{table_name}-HighReadCapacity",
        f"{table_name}-HighWriteCapacity",
        f"{table_name}-ReadThrottles",
        f"{table_name}-WriteThrottles",
        f"{table_name}-HighLatency"
    ]
    
    try:
        cloudwatch.delete_alarms(AlarmNames=alarm_names)
        print(f"Deleted {len(alarm_names)} CloudWatch alarms.")
    except Exception as e:
        print(f"Error deleting CloudWatch alarms: {e}")
        return False
    return True

def cleanup_autoscaling():
    """Clean up auto-scaling policies created in Lab 8."""
    print("\n=== Cleaning up Auto-scaling Policies ===")
    
    try:
        application_autoscaling = boto3.client('application-autoscaling')
        table_name = 'GameLeaderboard'
        
        # Delete scaling policies
        policies = [
            {'ResourceId': f'table/{table_name}', 'ScalableDimension': 'dynamodb:table:ReadCapacityUnits', 'PolicyName': 'ReadCapacityUtilization'},
            {'ResourceId': f'table/{table_name}', 'ScalableDimension': 'dynamodb:table:WriteCapacityUnits', 'PolicyName': 'WriteCapacityUtilization'}
        ]
        
        for policy in policies:
            try:
                application_autoscaling.delete_scaling_policy(
                    ServiceNamespace='dynamodb',
                    ResourceId=policy['ResourceId'],
                    ScalableDimension=policy['ScalableDimension'],
                    PolicyName=policy['PolicyName']
                )
            except Exception:
                pass  # Policy might not exist
        
        # Deregister scalable targets
        targets = [
            {'ResourceId': f'table/{table_name}', 'ScalableDimension': 'dynamodb:table:ReadCapacityUnits'},
            {'ResourceId': f'table/{table_name}', 'ScalableDimension': 'dynamodb:table:WriteCapacityUnits'}
        ]
        
        for target in targets:
            try:
                application_autoscaling.deregister_scalable_target(
                    ServiceNamespace='dynamodb',
                    ResourceId=target['ResourceId'],
                    ScalableDimension=target['ScalableDimension']
                )
            except Exception:
                pass  # Target might not exist
        
        print("Auto-scaling policies cleaned up.")
    except Exception as e:
        print(f"Error cleaning up auto-scaling: {e}")
        return False
    return True

def cleanup_resources():
    """Clean up all resources created during the DynamoDB features demo."""
    
    print("=== Comprehensive Cleanup of DynamoDB Demo Resources ===")
    
    success = True
    success &= cleanup_dynamodb_tables()
    success &= cleanup_cloudwatch_alarms()
    success &= cleanup_autoscaling()
    
    if success:
        print("\n=== Cleanup Complete ===")
        print("All resources created during the DynamoDB features demo have been removed.")
    else:
        print("\n=== Cleanup Completed with Errors ===")
        print("Some resources may still exist. Please check the AWS console.")
    
    return success

if __name__ == "__main__":
    # Ask for confirmation before proceeding
    confirm = input("This will delete the GameLeaderboard table and all its data. Continue? (y/n): ")
    
    if confirm.lower() != 'y':
        print("Cleanup cancelled.")
        sys.exit(0)
    
    success = cleanup_resources()
    
    if success:
        print("\nThank you for completing the DynamoDB features demo!")
    else:
        print("\nCleanup encountered errors. Some resources may still exist in your AWS account.")
        print("Please check the AWS Management Console to manually remove any remaining resources.")
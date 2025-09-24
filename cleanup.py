import sys
import os
import time
sys.path.append(os.path.dirname(__file__))
from utils.dynamodb_helper import get_dynamodb_client

def cleanup_resources():
    """Clean up all resources created during the DynamoDB features demo."""
    
    print("=== Cleaning up DynamoDB Resources ===")
    
    # Initialize DynamoDB client
    dynamodb = get_dynamodb_client()
    
    # Table name
    table_name = 'GameLeaderboard'
    
    # Check if table exists
    try:
        response = dynamodb.describe_table(TableName=table_name)
        table_exists = True
        print(f"Found table: {table_name}")
    except dynamodb.exceptions.ResourceNotFoundException:
        table_exists = False
        print(f"Table {table_name} does not exist. Nothing to clean up.")
    
    # Delete table if it exists
    if table_exists:
        try:
            print(f"Deleting table: {table_name}...")
            dynamodb.delete_table(TableName=table_name)
            
            # Wait for table to be deleted
            print("Waiting for table to be deleted...")
            waiter = dynamodb.get_waiter('table_not_exists')
            waiter.wait(TableName=table_name)
            
            print(f"Table {table_name} has been deleted successfully.")
        except Exception as e:
            print(f"Error deleting table: {e}")
            return False
    
    print("\n=== Cleanup Complete ===")
    print("All resources created during the DynamoDB features demo have been removed.")
    return True

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
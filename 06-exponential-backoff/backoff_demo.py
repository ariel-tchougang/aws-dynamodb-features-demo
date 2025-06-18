from datetime import datetime

import boto3
import time
from botocore.config import Config
from botocore.exceptions import ClientError

config = Config(retries=dict(max_attempts=10))  # DynamoDB default is 10

dynamodb = boto3.resource("dynamodb", config=config)
dynamodb_client = boto3.client("dynamodb", config=config)
table_name = "GameLeaderboard"
table = dynamodb.Table(table_name)

def main():
    """Demonstrate exponential backoff"""
    num_iterations = 200
    successful_requests = 0
    failed_requests = 0
    start_time = time.time()
    counter = 0

    while counter < num_iterations:
        counter += 1
        try:
            print(f"[{datetime.strftime(datetime.now(),'%H:%M:%S,%f')}] Get item")
            table.get_item(Key={"player_id": "pca974f2d", "game_id": "g81f00bfd"})
            successful_requests += 1
                
            # Small delay between requests to show progression
            # time.sleep(0.05)
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'ProvisionedThroughputExceededException':
                print(f"Request throttled: {e.response['Error']['Message']}")
                failed_requests += 1
            else:
                print(f"Error: {e}")
                failed_requests += 1
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    print("\n=== Results without Retry Configuration ===")
    print(f"Total requests: {num_iterations}")
    print(f"Successful requests: {successful_requests}")
    print(f"Failed requests: {failed_requests}")
    print(f"Total execution time: {execution_time:.2f} seconds")
    
    if failed_requests > 0:
        print("\n⚠️ Some requests failed due to throttling.")
        print("This demonstrates why retry configuration is important when working with DynamoDB.")
    else:
        print("\n✅ All requests succeeded without throttling.")
        print("Try increasing the number of concurrent requests to trigger throttling.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        exit(0)
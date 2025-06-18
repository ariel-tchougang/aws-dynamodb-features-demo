# Lab 6: Exponential Backoff and Retry

In this lab, you'll learn how to handle throttling errors (HTTP 429 - ProvisionedThroughputExceededException) using the AWS SDK's built-in exponential backoff and retry mechanism.

## What is Exponential Backoff?

Exponential backoff is a strategy where a client automatically retries a failed request, but with progressively longer wait times between retries. This helps to:

1. Avoid overwhelming the service with retry requests
2. Allow the service time to recover
3. Increase the chances of eventual success

## Lab Setup

In this lab, we'll:

1. Set a low provisioned throughput for our table (1 RCU)
2. Generate a high volume of read requests
3. Configure the AWS SDK's retry mechanism
4. Observe how the system handles throttling

## Instructions

### Step 1: Update Table to Low Throughput

First, update the table to have a very low read capacity:

```bash
aws dynamodb update-table \
    --table-name GameLeaderboard \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=5
```

```PowerShell
aws dynamodb update-table `
  --table-name "GameLeaderboard" `
  --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=5
```

Wait for the table to finish updating:

```bash
#Active wait
aws dynamodb wait table-exists --table-name GameLeaderboard

aws dynamodb describe-table \
    --table-name GameLeaderboard \
    --query "Table.TableStatus"
```

```bash
#Active wait
aws dynamodb wait table-exists --table-name GameLeaderboard

aws dynamodb describe-table `
    --table-name GameLeaderboard `
    --query "Table.TableStatus"
```

### Step 2: Run Requests Without Retry Logic

Run the provided script to generate read requests without proper retry logic:

```bash
python no_retry.py
```

You should see several ProvisionedThroughputExceededException errors.

### Step 3: Run Requests With AWS SDK's Retry Configuration

Now run the script that uses the AWS SDK's built-in retry mechanism:

```bash
python with_retry.py
```

Observe how the SDK handles throttling by:
1. Catching the ProvisionedThroughputExceededException
2. Automatically implementing exponential backoff with jitter
3. Eventually succeeding with all requests

### Step 4: Analyze the Results

Compare the results of both approaches:

1. Without retry: Many failed requests
2. With SDK retry configuration: All requests eventually succeed

## AWS SDK Retry Configuration

The AWS SDK for Python (Boto3) provides built-in retry capabilities that you can configure:

```python
from botocore.config import Config

# Configure retry strategy
config = Config(
    retries={
        'max_attempts': 10,     # Maximum number of retry attempts
        'mode': 'standard'      # Uses exponential backoff with jitter
    }
)

# Initialize DynamoDB with retry configuration
dynamodb = boto3.resource('dynamodb', config=config)
```

### Retry Modes

The SDK supports different retry modes:

- **'legacy'**: The original retry behavior
- **'standard'**: Exponential backoff with jitter (recommended)
- **'adaptive'**: Dynamically adjusts retry rate based on observed throttling

## Best Practices for Handling Throttling

1. **Use the SDK's built-in retry mechanism** rather than implementing your own
2. **Configure appropriate max_attempts** based on your application's needs
3. **Consider using adaptive mode** for high-throughput applications
4. **Set reasonable timeouts** to avoid waiting too long for retries
5. **Consider using DynamoDB auto-scaling** for production workloads
6. **Monitor throttling events** in CloudWatch to adjust capacity

## Restore Table Capacity

After completing this lab, restore the table's capacity to normal:

```bash
aws dynamodb update-table \
    --table-name GameLeaderboard \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

## Next Steps

Once you've completed this lab, proceed to [Lab 7: Parallel Scan](../07-parallel-scan/) to learn how to improve scan performance with parallel processing.
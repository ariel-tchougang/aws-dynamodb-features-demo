# Lab 7: Parallel Scan in DynamoDB

In this lab, you'll learn how to use parallel scan to improve the performance of scan operations in DynamoDB, especially for large tables.

## What is Parallel Scan?

Parallel scan allows you to split a scan operation into multiple segments that can be processed simultaneously. This can significantly improve performance for large tables by:

1. Distributing the read workload across multiple workers
2. Utilizing your provisioned throughput more efficiently
3. Reducing the overall time needed to scan a table

## Lab Overview

In this lab, you'll:

1. Perform a standard sequential scan of the table
2. Implement a parallel scan with multiple segments
3. Compare the performance between sequential and parallel scans

## Instructions

### Step 1: Restore Table Capacity

If you reduced the table's capacity in the previous lab, restore it first:

```bash
aws dynamodb update-table \
    --table-name GameLeaderboard \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

### Step 2: Run a Sequential Scan

Run the provided script to perform a standard sequential scan:

```bash
python sequential_scan.py
```

This will scan the entire table and measure the time taken.

### Step 3: Run a Parallel Scan

Now run the script that implements parallel scan:

```bash
python parallel_scan.py
```

This will:
1. Split the scan into multiple segments
2. Process each segment in parallel using threads
3. Measure the total time taken

### Step 4: Compare Results

The scripts will output performance metrics that you can compare:

- Total execution time
- Items processed per second
- Consumed read capacity units

## How Parallel Scan Works

A parallel scan operation uses two parameters:

1. **TotalSegments**: The total number of segments to split the table into
2. **Segment**: The specific segment to scan (0 to TotalSegments-1)

Each worker processes a different segment:

```python
# Worker for segment 0
response = table.scan(
    TotalSegments=4,
    Segment=0
)

# Worker for segment 1
response = table.scan(
    TotalSegments=4,
    Segment=1
)

# And so on...
```

## Best Practices for Parallel Scan

1. **Choose the right number of segments**: Start with the number of workers you plan to use
2. **Monitor consumed capacity**: Parallel scan can consume a lot of RCUs quickly
3. **Consider table size**: For small tables, the overhead might outweigh the benefits
4. **Use consistent read if needed**: Set `ConsistentRead=True` if you need consistency
5. **Implement pagination**: Each segment might return multiple pages of results

## Code Example

Here's a simplified example of parallel scan implementation:

```python
import boto3
import threading

def scan_segment(segment, total_segments, results):
    """Scan a specific segment of the table."""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    response = table.scan(
        TotalSegments=total_segments,
        Segment=segment
    )
    
    # Process items from this segment
    items = response['Items']
    
    # Continue scanning if we have more items in this segment
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            TotalSegments=total_segments,
            Segment=segment,
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        items.extend(response['Items'])
    
    # Add results from this segment to the shared results list
    results.extend(items)

def parallel_scan(total_segments):
    """Perform a parallel scan using multiple threads."""
    threads = []
    results = []
    
    # Create and start a thread for each segment
    for segment in range(total_segments):
        thread = threading.Thread(
            target=scan_segment,
            args=(segment, total_segments, results)
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    return results
```

## Next Steps

Once you've completed this lab, proceed to [Lab 8: Auto-scaling](../08-auto-scaling/) to learn how DynamoDB can automatically adjust capacity based on workload.
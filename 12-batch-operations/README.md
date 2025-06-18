# Lab 12: Batch Operations in DynamoDB

In this lab, you'll learn how to use batch operations in DynamoDB to efficiently read and write multiple items in a single API call.

## What are Batch Operations?

DynamoDB provides two batch operations:

1. **BatchGetItem** - Retrieve multiple items from one or more tables
2. **BatchWriteItem** - Put or delete multiple items in one or more tables

These operations help you:
- Reduce the number of network round trips
- Improve throughput
- Simplify application code

## Lab Overview

In this lab, you'll:

1. Use BatchGetItem to retrieve multiple items efficiently
2. Use BatchWriteItem to write multiple items in one request
3. Handle unprocessed items
4. Compare performance with individual operations

## Instructions

### Step 1: Run Batch Get Example

Run the provided script to see BatchGetItem in action:

```bash
python batch_get.py
```

This will demonstrate:
- Retrieving multiple items in a single API call
- Handling unprocessed items
- Comparing performance with individual GetItem calls

### Step 2: Run Batch Write Example

Run the provided script to see BatchWriteItem in action:

```bash
python batch_write.py
```

This will demonstrate:
- Writing multiple items in a single API call
- Handling unprocessed items
- Comparing performance with individual PutItem calls

## Batch Operation Limitations

- **BatchGetItem**: Maximum of 100 items or 16 MB of data
- **BatchWriteItem**: Maximum of 25 put or delete operations
- No transaction support (not atomic)
- No support for update operations
- No support for conditional expressions

## Next Steps

Once you've completed this lab, proceed to [Lab 13: CloudWatch Metrics](../13-cloudwatch-metrics/) to learn how to monitor DynamoDB performance.
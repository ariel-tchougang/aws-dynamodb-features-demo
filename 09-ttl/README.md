# Lab 9: Time to Live (TTL) in DynamoDB

In this lab, you'll learn how to use DynamoDB's Time to Live (TTL) feature to automatically expire and delete items from your table.

## What is Time to Live (TTL)?

Time to Live (TTL) allows you to define a per-item timestamp to determine when an item is no longer needed. DynamoDB automatically deletes expired items without consuming write throughput. This helps you:

1. Reduce storage costs by automatically removing obsolete data
2. Implement data lifecycle policies
3. Maintain compliance with data retention requirements

## Lab Overview

In this lab, you'll:

1. Enable TTL on your DynamoDB table
2. Add items with expiration timestamps
3. Observe the automatic deletion of expired items
4. Monitor TTL metrics in CloudWatch

## Instructions

### Step 1: Enable TTL on the Table

Run the provided script to enable TTL on your table:

```bash
python enable_ttl.py
```

This will configure the `expiration_time` attribute as the TTL attribute for the table.

### Step 2: Add Items with TTL Values

Run the provided script to add items with various expiration times:

```bash
python add_items_with_ttl.py
```

This will:
- Add items that expire in 2 minutes
- Add items that expire in 5 minutes
- Add items that expire in 10 minutes
- Add items with no expiration

### Step 3: Monitor TTL Deletions

Run the provided script to monitor the TTL process:

```bash
python monitor_ttl.py
```

This will:
- Count items before expiration
- Wait for the TTL process to run
- Count items after expiration
- Show CloudWatch metrics for TTL deletions

## How TTL Works

1. You define a specific attribute to store the expiration time as an epoch timestamp (seconds since Jan 1, 1970)
2. DynamoDB compares the current time with the TTL attribute value
3. Items where the TTL value is older than the current time are marked for deletion
4. A background process deletes the expired items, typically within 48 hours
5. No write throughput is consumed for TTL deletions

## Next Steps

Once you've completed this lab, proceed to [Lab 10: Transactions](../10-transactions/) to learn how to perform atomic operations across multiple items.
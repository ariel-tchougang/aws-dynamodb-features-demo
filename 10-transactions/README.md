# Lab 10: DynamoDB Transactions

In this lab, you'll learn how to use DynamoDB transactions to perform atomic operations across multiple items.

## What are DynamoDB Transactions?

DynamoDB transactions provide atomicity, consistency, isolation, and durability (ACID) across multiple operations on items in one or more tables. This ensures that:

1. All operations succeed or none of them do
2. Changes are isolated from other operations
3. Data remains consistent before and after the transaction

## Lab Overview

In this lab, you'll:

1. Create a game reward system that requires transactional consistency
2. Implement TransactWriteItems for atomic operations
3. Implement TransactGetItems for consistent reads
4. Handle transaction conflicts and failures

## Instructions

### Step 1: Set Up Transaction Tables

Run the provided script to create additional tables for our transaction demo:

```bash
python setup_transaction_tables.py
```

This will create:
- `PlayerInventory` table - Stores player items and currency
- `GameAchievements` table - Stores achievement records

### Step 2: Run Transaction Examples

Run the provided script to see transactions in action:

```bash
python run_transactions.py
```

This will demonstrate:
- Awarding items and currency atomically
- Transferring items between players
- Reading multiple items consistently

### Step 3: Test Transaction Failures

Run the provided script to see how transaction failures are handled:

```bash
python test_transaction_failures.py
```

This will demonstrate:
- Condition check failures
- Transaction cancellation
- Error handling

## Next Steps

Once you've completed this lab, proceed to [Lab 11: Conditional Operations](../11-conditional-operations/) to learn how to perform conditional writes in DynamoDB.
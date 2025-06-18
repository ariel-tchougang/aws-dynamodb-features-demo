# Lab 4: Query Performance Testing

In this lab, you'll compare the performance of different query access patterns in DynamoDB using the primary key and Global Secondary Index (GSI).

## Query Access Patterns

We'll test two different access patterns:

1. **Access Pattern 1**: Find all games for a specific player
   - Query using the primary key (partition key: `player_id`)
   - Query using the GSI (partition key: `game_date`)

2. **Access Pattern 2**: Find all games played on a specific date
   - Query using the primary key (filtering by `game_date`)
   - Query using the GSI (partition key: `game_date`)

## Instructions

### Access Pattern 1: Find all games for a specific player

#### Query using Primary Key:

```bash
# Using AWS CLI
aws dynamodb query \
    --table-name GameLeaderboard \
    --key-condition-expression "player_id = :pid" \
    --expression-attribute-values '{":pid": {"S": "p12345678"}}' \
    --return-consumed-capacity TOTAL
```

#### Query using GSI (less efficient for this pattern):

```bash
# Using AWS CLI - This is inefficient and requires client-side filtering
aws dynamodb scan \
    --table-name GameLeaderboard \
    --filter-expression "player_id = :pid" \
    --expression-attribute-values '{":pid": {"S": "p12345678"}}' \
    --return-consumed-capacity TOTAL
```

### Access Pattern 2: Find all games played on a specific date

#### Query using Primary Key (less efficient for this pattern):

```bash
# Using AWS CLI - This is inefficient and requires a scan with filter
aws dynamodb scan \
    --table-name GameLeaderboard \
    --filter-expression "game_date = :date" \
    --expression-attribute-values '{":date": {"S": "2023-05-15"}}' \
    --return-consumed-capacity TOTAL
```

#### Query using GSI (more efficient for this pattern):

```bash
# Using AWS CLI
aws dynamodb query \
    --table-name GameLeaderboard \
    --index-name GameDateIndex \
    --key-condition-expression "game_date = :date" \
    --expression-attribute-values '{":date": {"S": "2023-05-15"}}' \
    --return-consumed-capacity TOTAL
```

## Performance Comparison

We've provided Python scripts to run these queries and measure their performance:

- `query_by_player.py` - Compares querying by player using primary key vs. scan
- `query_by_date.py` - Compares querying by date using scan vs. GSI

Run these scripts to see the performance difference:

```bash
python query_by_player.py
python query_by_date.py
```

## Expected Results

You should observe:

1. For Access Pattern 1 (finding games by player):
   - The primary key query is significantly faster and consumes fewer RCUs
   - The scan operation is slower and consumes more RCUs

2. For Access Pattern 2 (finding games by date):
   - The GSI query is significantly faster and consumes fewer RCUs
   - The scan with filter is slower and consumes more RCUs

## Key Takeaways

- Choose the right access pattern for your query needs
- Design your table and indexes based on your most common query patterns
- Using the wrong access pattern can result in higher latency and costs
- GSIs are powerful for enabling efficient queries on non-key attributes

## Next Steps

Once you've completed this lab, proceed to [Lab 5: Scan Operations](../05-scan-operations/) to learn more about scan operations and pagination.
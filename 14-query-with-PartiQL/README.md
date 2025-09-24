# Lab 14: PartiQL Queries

In this lab, you'll learn how to use PartiQL, a SQL-compatible query language, to interact with DynamoDB tables using familiar SQL syntax.

## What is PartiQL?

PartiQL is a SQL-compatible query language that makes it easy to query data across different data stores. For DynamoDB, PartiQL provides:

1. Familiar SQL syntax for developers
2. Support for SELECT, INSERT, UPDATE, and DELETE operations
3. Ability to work with nested data structures
4. Integration with existing DynamoDB features

## Lab Overview

In this lab, you'll:

1. Execute various PartiQL SELECT queries
2. Perform INSERT, UPDATE, and DELETE operations
3. Work with filtering and projections
4. Use PartiQL with indexes
5. Test queries in NoSQL Workbench

## Instructions

### Step 1: Run PartiQL Examples

Execute the provided Python script to see various PartiQL operations:

```bash
python partiql_examples.py
```

This script demonstrates:
- Basic SELECT queries
- Filtering with WHERE clauses
- Using ORDER BY with indexes
- INSERT, UPDATE, and DELETE operations
- Working with parameters

### Step 2: Test Queries in NoSQL Workbench

Use the provided text file with ready-to-use PartiQL queries:

1. Open NoSQL Workbench for DynamoDB
2. Connect to your table
3. Copy queries from `partiql_queries.txt`
4. Execute them in the PartiQL editor

## PartiQL Query Examples

### Basic SELECT Operations

```sql
-- Select all items
SELECT * FROM GameLeaderboard

-- Select specific attributes
SELECT player_id, player_name, score FROM GameLeaderboard

-- Select with filtering
SELECT * FROM GameLeaderboard WHERE score > 9000
```

### Using Indexes

```sql
-- Query using Global Secondary Index
SELECT * FROM GameLeaderboard.GameDateIndex 
WHERE game_date = '2024-01-15' 
ORDER BY score DESC
```

### Data Modification

```sql
-- Insert new item
INSERT INTO GameLeaderboard VALUE {
    'player_id': 'new_player',
    'game_id': 'new_game',
    'player_name': 'New Player',
    'score': 8500
}

-- Update existing item
UPDATE GameLeaderboard 
SET score = 9500 
WHERE player_id = 'player123' AND game_id = 'game456'

-- Delete item
DELETE FROM GameLeaderboard 
WHERE player_id = 'player123' AND game_id = 'game456'
```

## Key PartiQL Features

- **SQL Compatibility** - Use familiar SQL syntax
- **Parameter Binding** - Safely pass parameters using `?` placeholders
- **Index Support** - Query Global and Local Secondary Indexes
- **Nested Data** - Work with complex data structures
- **DynamoDB Integration** - Full compatibility with DynamoDB features

## Best Practices

1. Use parameter binding to prevent injection attacks
2. Leverage indexes for efficient queries
3. Be mindful of scan vs. query operations
4. Use projections to reduce data transfer
5. Consider pagination for large result sets

## Next Steps

Congratulations! You've completed all the labs in this DynamoDB features demo. You now have hands-on experience with a wide range of DynamoDB features and best practices.

To clean up all resources created during these labs, run:

```bash
python ../cleanup.py
```
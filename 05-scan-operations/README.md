# Lab 5: DynamoDB Scan Operations

In this lab, you'll explore various scan operations in DynamoDB, including pagination, filtering, and projection.

## Scan Operations Overview

1. **Simple Scan** - Retrieve all items from the table
2. **Scan with Page Size** - Control the number of items per API call
3. **Scan with Max Items** - Limit the number of items returned and get a continuation token
4. **Scan with Starting Token** - Continue a scan from a previous position
5. **Scan with Filter Expression** - Filter items on the server side after retrieval
6. **Scan with Projection Expression** - Retrieve only specific attributes

## Instructions

### 1. Simple Scan

#### Using AWS CLI:

```bash
aws dynamodb scan \
    --table-name GameLeaderboard \
    --return-consumed-capacity TOTAL
```

```PowerShell
aws dynamodb scan `
    --table-name GameLeaderboard `
    --return-consumed-capacity TOTAL
```

#### Using Python with Boto3:

```python
import boto3

def simple_scan():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    response = table.scan(
        ReturnConsumedCapacity='TOTAL'
    )
    
    print(f"Items retrieved: {len(response['Items'])}")
    print(f"Consumed capacity: {response['ConsumedCapacity']['CapacityUnits']} RCUs")

simple_scan()
```

### 2. Scan with Page Size

#### Using AWS CLI:

```bash
aws dynamodb scan \
    --table-name GameLeaderboard \
    --page-size 2 \
    --projection-expression "player_id, player_name, score" \
    --return-consumed-capacity TOTAL
```

```PowerShell
aws dynamodb scan `
    --table-name GameLeaderboard `
    --page-size 2 `
    --projection-expression "player_id, player_name, score" `
    --return-consumed-capacity TOTAL
```

#### Using Python with Boto3:

```python
import boto3

def scan_with_page_size():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    # Track API calls
    api_calls = 0
    total_items = 0
    
    # Scan with small page size to demonstrate multiple API calls
    response = table.scan(
        ReturnConsumedCapacity='TOTAL',
        Limit=10  # Small page size to force multiple API calls
    )
    
    api_calls += 1
    total_items += len(response['Items'])
    print(f"API call {api_calls}: Retrieved {len(response['Items'])} items")
    
    # Continue scanning if we have more items
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ExclusiveStartKey=response['LastEvaluatedKey'],
            ReturnConsumedCapacity='TOTAL',
            Limit=10
        )
        
        api_calls += 1
        total_items += len(response['Items'])
        print(f"API call {api_calls}: Retrieved {len(response['Items'])} items")
    
    print(f"\nTotal API calls: {api_calls}")
    print(f"Total items retrieved: {total_items}")

scan_with_page_size()
```

### 3. Scan with Max Items

#### Using AWS CLI:

```bash
aws dynamodb scan \
    --table-name GameLeaderboard \
    --max-items 20 \
    --return-consumed-capacity TOTAL
```

```PowerShell
aws dynamodb scan `
    --table-name GameLeaderboard `
    --projection-expression "player_id, player_name, score" `
    --max-items 20 `
    --return-consumed-capacity TOTAL
```

#### Using Python with Boto3:

```python
import boto3

def scan_with_max_items():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    # Scan with max items limit
    response = table.scan(
        ReturnConsumedCapacity='TOTAL',
        Limit=20  # Limit to 20 items
    )
    
    print(f"Items retrieved: {len(response['Items'])}")
    print(f"Consumed capacity: {response['ConsumedCapacity']['CapacityUnits']} RCUs")
    
    if 'LastEvaluatedKey' in response:
        print("\nNot all items retrieved. Last evaluated key:")
        print(response['LastEvaluatedKey'])
        print("Use this key with ExclusiveStartKey to continue the scan")

scan_with_max_items()
```

### 4. Scan with Starting Token

#### Using AWS CLI:

```bash
# First scan to get the continuation token
aws dynamodb scan \
    --table-name GameLeaderboard \
    --max-items 20 \
    --return-consumed-capacity TOTAL

# Then use the continuation token to get the next set of items
aws dynamodb scan \
    --table-name GameLeaderboard \
    --starting-token "eyJwbGF5ZXJfaWQiOnsiUyI6InAxMjM0NTY3OCJ9LCJnYW1lX2lkIjp7IlMiOiJnODc2NTQzMjEifX0=" \
    --max-items 20
```

```PowerShell
# First scan to get the continuation token
aws dynamodb scan `
    --table-name GameLeaderboard `
    --max-items 1 `
    --projection-expression "player_id, player_name, score" `
    --return-consumed-capacity TOTAL

# Then use the continuation token to get the next set of items
aws dynamodb scan `
    --table-name GameLeaderboard `
    --starting-token "eyJFeGNsdXNpdmVTdGFydEtleSI6IG51bGwsICJib3RvX3RydW5jYXRlX2Ftb3VudCI6IDF9" `
    --projection-expression "player_id, player_name, score" `
    --max-items 5
```

#### Using Python with Boto3:

```python
import boto3
import json

def scan_with_starting_token():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    # First scan to get a starting token
    print("First scan (20 items):")
    response = table.scan(
        ReturnConsumedCapacity='TOTAL',
        Limit=20
    )
    
    print(f"Items retrieved: {len(response['Items'])}")
    
    # Check if we have more items
    if 'LastEvaluatedKey' in response:
        last_key = response['LastEvaluatedKey']
        print("\nContinuation token (LastEvaluatedKey):")
        print(json.dumps(last_key))
        
        # Continue scan with the LastEvaluatedKey
        print("\nContinuing scan with LastEvaluatedKey:")
        response2 = table.scan(
            ExclusiveStartKey=last_key,
            ReturnConsumedCapacity='TOTAL',
            Limit=20
        )
        
        print(f"Additional items retrieved: {len(response2['Items'])}")
        
        # Check if we have even more items
        if 'LastEvaluatedKey' in response2:
            print("\nMore items available. Scan can be continued.")
        else:
            print("\nNo more items to retrieve.")

scan_with_starting_token()
```

### 5. Scan with Filter Expression

#### Using AWS CLI:

```bash
aws dynamodb scan \
    --table-name GameLeaderboard \
    --filter-expression "score > :min_score" \
    --expression-attribute-values '{":min_score": {"N": "9000"}}' \
    --return-consumed-capacity TOTAL
```

```PowerShell
aws dynamodb scan `
    --table-name GameLeaderboard `
    --filter-expression "score > :min_score" `
    --expression-attribute-values '{\":min_score\": {\"N\": \"9950\"}}' `
    --return-consumed-capacity TOTAL
```

#### Using Python with Boto3:

```python
import boto3
from boto3.dynamodb.conditions import Key, Attr

def scan_with_filter():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    # Scan with filter expression
    response = table.scan(
        FilterExpression=Attr('score').gt(9000),
        ReturnConsumedCapacity='TOTAL'
    )
    
    print(f"Items scanned: {response['ScannedCount']}")
    print(f"Items matching filter: {len(response['Items'])}")
    print(f"Consumed capacity: {response['ConsumedCapacity']['CapacityUnits']} RCUs")
    
    # Calculate filter efficiency
    filter_efficiency = len(response['Items']) / response['ScannedCount'] * 100
    print(f"\nFilter efficiency: {filter_efficiency:.2f}%")
    print("Note: Filter expressions are applied AFTER items are read from the table.")
    print("You are charged for reading ALL items, even if they don't match the filter.")

scan_with_filter()
```

### 6. Scan with Projection Expression

#### Using AWS CLI:

```bash
aws dynamodb scan \
    --table-name GameLeaderboard \
    --projection-expression "player_id, player_name, score" \
    --return-consumed-capacity TOTAL
```

```PowerShell
aws dynamodb scan `
    --table-name GameLeaderboard `
    --filter-expression "score > :min_score" `
    --expression-attribute-values '{\":min_score\": {\"N\": \"9950\"}}' `
    --projection-expression "player_id, player_name, score" `
    --return-consumed-capacity TOTAL
```

#### Using Python with Boto3:

```python
import boto3

def scan_with_projection():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    # Scan with projection expression
    response = table.scan(
        ProjectionExpression="player_id, player_name, score",
        ReturnConsumedCapacity='TOTAL'
    )
    
    print(f"Items retrieved: {len(response['Items'])}")
    print(f"Consumed capacity: {response['ConsumedCapacity']['CapacityUnits']} RCUs")
    
    # Show the first few items to demonstrate projection
    print("\nSample items (with only projected attributes):")
    for item in response['Items'][:3]:
        print(item)

scan_with_projection()
```

## Running the Examples

We've provided Python scripts for each scan operation:

- `simple_scan.py` - Basic scan operation
- `scan_with_page_size.py` - Scan with pagination
- `scan_with_max_items.py` - Scan with item limit
- `scan_with_starting_token.py` - Scan with continuation
- `scan_with_filter.py` - Scan with filtering
- `scan_with_projection.py` - Scan with attribute projection

Run each script to see the operation in action:

```bash
python simple_scan.py
python scan_with_page_size.py
python scan_with_max_items.py
python scan_with_starting_token.py
python scan_with_filter.py
python scan_with_projection.py
```

## Next Steps

Once you've mastered scan operations, proceed to [Lab 6: Exponential Backoff](../06-exponential-backoff/) to learn how to handle throttling with retry mechanisms.
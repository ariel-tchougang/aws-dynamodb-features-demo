# Lab 3: Basic CRUD Operations in DynamoDB

In this lab, you'll learn how to perform basic Create, Read, Update, and Delete (CRUD) operations on your `GameLeaderboard` table using both AWS CLI and Python with Boto3.

## Operations Overview

1. **Create (Put Item)** - Add a new game record to the table
2. **Read (Get Item)** - Retrieve a specific game record
3. **Update (Update Item)** - Modify an existing game record
4. **Delete (Delete Item)** - Remove a game record from the table

## Instructions

### 1. Create (Put Item)

#### Using AWS CLI:

```bash
aws dynamodb put-item \
    --table-name GameLeaderboard \
    --item '{
        "player_id": {"S": "p12345678"},
        "game_id": {"S": "g87654321"},
        "player_name": {"S": "NewPlayer123"},
        "game_date": {"S": "2023-06-01"},
        "score": {"N": "9500"},
        "game_duration": {"N": "450"},
        "achievements": {"L": [{"S": "FirstBlood"}, {"S": "Survivor"}]},
        "game_mode": {"S": "battle-royale"},
        "expiration_time": {"N": "0"},
        "last_updated": {"S": "2023-06-01T10:15:30Z"}
    }'
```

#### Using Python with Boto3:

```python
import boto3
from decimal import Decimal

def put_item():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    response = table.put_item(
        Item={
            'player_id': 'p12345678',
            'game_id': 'g87654321',
            'player_name': 'NewPlayer123',
            'game_date': '2023-06-01',
            'score': Decimal('9500'),
            'game_duration': Decimal('450'),
            'achievements': ['FirstBlood', 'Survivor'],
            'game_mode': 'battle-royale',
            'expiration_time': Decimal('0'),
            'last_updated': '2023-06-01T10:15:30Z'
        }
    )
    
    print("Put Item succeeded:")
    print(response)

put_item()
```

### 2. Read (Get Item)

#### Using AWS CLI:

```bash
aws dynamodb get-item \
    --table-name GameLeaderboard \
    --key '{
        "player_id": {"S": "p12345678"},
        "game_id": {"S": "g87654321"}
    }'
```

#### Using Python with Boto3:

```python
import boto3
import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def get_item():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    response = table.get_item(
        Key={
            'player_id': 'p12345678',
            'game_id': 'g87654321'
        }
    )
    
    if 'Item' in response:
        print("Get Item succeeded:")
        print(json.dumps(response['Item'], indent=4, cls=DecimalEncoder))
    else:
        print("Item not found")

get_item()
```

### 3. Update (Update Item)

#### Using AWS CLI:

```bash
aws dynamodb update-item \
    --table-name GameLeaderboard \
    --key '{
        "player_id": {"S": "p12345678"},
        "game_id": {"S": "g87654321"}
    }' \
    --update-expression "SET score = :s, achievements = :a, last_updated = :lu" \
    --expression-attribute-values '{
        ":s": {"N": "9800"},
        ":a": {"L": [{"S": "FirstBlood"}, {"S": "Survivor"}, {"S": "MVP"}]},
        ":lu": {"S": "2023-06-01T11:30:45Z"}
    }' \
    --return-values ALL_NEW
```

#### Using Python with Boto3:

```python
import boto3
import json
from decimal import Decimal
from datetime import datetime

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def update_item():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    response = table.update_item(
        Key={
            'player_id': 'p12345678',
            'game_id': 'g87654321'
        },
        UpdateExpression="SET score = :s, achievements = :a, last_updated = :lu",
        ExpressionAttributeValues={
            ':s': Decimal('9800'),
            ':a': ['FirstBlood', 'Survivor', 'MVP'],
            ':lu': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        },
        ReturnValues="ALL_NEW"
    )
    
    print("Update Item succeeded:")
    print(json.dumps(response['Attributes'], indent=4, cls=DecimalEncoder))

update_item()
```

### 4. Delete (Delete Item)

#### Using AWS CLI:

```bash
aws dynamodb delete-item \
    --table-name GameLeaderboard \
    --key '{
        "player_id": {"S": "p12345678"},
        "game_id": {"S": "g87654321"}
    }' \
    --return-values ALL_OLD
```

#### Using Python with Boto3:

```python
import boto3
import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def delete_item():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameLeaderboard')
    
    response = table.delete_item(
        Key={
            'player_id': 'p12345678',
            'game_id': 'g87654321'
        },
        ReturnValues="ALL_OLD"
    )
    
    if 'Attributes' in response:
        print("Delete Item succeeded:")
        print(json.dumps(response['Attributes'], indent=4, cls=DecimalEncoder))
    else:
        print("Item not found or already deleted")

delete_item()
```

## Running the Examples

We've provided Python scripts for each operation:

- `put_item.py` - Create a new game record
- `get_item.py` - Read a specific game record
- `update_item.py` - Update an existing game record
- `delete_item.py` - Delete a game record

Run each script to see the operation in action:

```bash
python put_item.py
python get_item.py
python update_item.py
python delete_item.py
```

## Next Steps

Once you've mastered basic CRUD operations, proceed to [Lab 4: Query Performance](../04-query-performance/) to learn about querying data and comparing performance between different access patterns.
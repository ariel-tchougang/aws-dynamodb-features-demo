import sys
import os
import json
from decimal import Decimal
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.dynamodb_helper import get_dynamodb_client

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def execute_partiql_query(statement, parameters=None):
    """Execute a PartiQL statement and return results."""
    dynamodb = get_dynamodb_client()
    
    try:
        if parameters:
            response = dynamodb.execute_statement(
                Statement=statement,
                Parameters=parameters
            )
        else:
            response = dynamodb.execute_statement(Statement=statement)
        
        return response['Items']
    except Exception as e:
        print(f"Error executing query: {e}")
        return []

def partiql_examples():
    """Demonstrate various PartiQL queries on GameLeaderboard table."""
    
    print("=== PartiQL Query Examples ===\n")
    
    # 1. SELECT all items
    print("1. SELECT all items:")
    statement = "SELECT * FROM GameLeaderboard"
    items = execute_partiql_query(statement)
    print(f"Query: {statement}")
    print(f"Results: {len(items)} items")
    if items:
        print(json.dumps(items[0], indent=2, cls=DecimalEncoder))
    print()
    
    # 2. SELECT with WHERE clause
    print("2. SELECT with WHERE clause (high scores):")
    statement = "SELECT * FROM GameLeaderboard WHERE score > ?"
    parameters = [{'N': '9000'}]
    items = execute_partiql_query(statement, parameters)
    print(f"Query: {statement}")
    print(f"Parameters: score > 9000")
    print(f"Results: {len(items)} items")
    print()
    
    # 3. SELECT specific attributes
    print("3. SELECT specific attributes:")
    statement = "SELECT player_id, player_name, score FROM GameLeaderboard"
    items = execute_partiql_query(statement)
    print(f"Query: {statement}")
    print(f"Results: {len(items)} items")
    if items:
        print(json.dumps(items[0], indent=2, cls=DecimalEncoder))
    print()
    
    # 4. SELECT with ORDER BY (using GSI)
    print("4. SELECT with ORDER BY using GSI:")
    statement = "SELECT * FROM GameLeaderboard.GameDateIndex WHERE game_date = ? ORDER BY score DESC"
    parameters = [{'S': '2024-01-15'}]
    items = execute_partiql_query(statement, parameters)
    print(f"Query: {statement}")
    print(f"Parameters: game_date = '2024-01-15'")
    print(f"Results: {len(items)} items")
    print()
    
    # 5. SELECT with LIMIT
    print("5. SELECT with LIMIT:")
    statement = "SELECT * FROM GameLeaderboard LIMIT 5"
    items = execute_partiql_query(statement)
    print(f"Query: {statement}")
    print(f"Results: {len(items)} items")
    print()
    
    # 6. SELECT with multiple conditions
    print("6. SELECT with multiple conditions:")
    statement = "SELECT * FROM GameLeaderboard WHERE player_id = ? AND game_id = ?"
    parameters = [{'S': 'player123'}, {'S': 'game456'}]
    items = execute_partiql_query(statement, parameters)
    print(f"Query: {statement}")
    print(f"Parameters: player_id = 'player123' AND game_id = 'game456'")
    print(f"Results: {len(items)} items")
    print()
    
    # 7. INSERT item
    print("7. INSERT new item:")
    statement = """
    INSERT INTO GameLeaderboard VALUE {
        'player_id': ?,
        'game_id': ?,
        'player_name': ?,
        'score': ?,
        'game_date': ?,
        'level_completed': ?
    }
    """
    parameters = [
        {'S': 'partiql_player'},
        {'S': 'partiql_game'},
        {'S': 'PartiQL Tester'},
        {'N': '8500'},
        {'S': '2024-01-20'},
        {'N': '15'}
    ]
    try:
        dynamodb = get_dynamodb_client()
        response = dynamodb.execute_statement(
            Statement=statement,
            Parameters=parameters
        )
        print("INSERT successful")
    except Exception as e:
        print(f"INSERT failed: {e}")
    print()
    
    # 8. UPDATE item
    print("8. UPDATE item:")
    statement = "UPDATE GameLeaderboard SET score = ? WHERE player_id = ? AND game_id = ?"
    parameters = [{'N': '9500'}, {'S': 'partiql_player'}, {'S': 'partiql_game'}]
    try:
        dynamodb = get_dynamodb_client()
        response = dynamodb.execute_statement(
            Statement=statement,
            Parameters=parameters
        )
        print("UPDATE successful")
    except Exception as e:
        print(f"UPDATE failed: {e}")
    print()
    
    # 9. DELETE item
    print("9. DELETE item:")
    statement = "DELETE FROM GameLeaderboard WHERE player_id = ? AND game_id = ?"
    parameters = [{'S': 'partiql_player'}, {'S': 'partiql_game'}]
    try:
        dynamodb = get_dynamodb_client()
        response = dynamodb.execute_statement(
            Statement=statement,
            Parameters=parameters
        )
        print("DELETE successful")
    except Exception as e:
        print(f"DELETE failed: {e}")
    print()

def get_dynamodb_client():
    """Return a DynamoDB client."""    

    # set aws profile
    # boto3.setup_default_session(profile_name='your_profile')

    # dynamodb = boto3.client('dynamodb')
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')

    # set region and endpoint_url
    #dynamodb = boto3.client('dynamodb', region_name='eu-west-3', endpoint_url='http://localhost:8000')
    
    return dynamodb

if __name__ == "__main__":
    partiql_examples()
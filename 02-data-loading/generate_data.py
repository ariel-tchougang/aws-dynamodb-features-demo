import json
import random
import uuid
from datetime import datetime, timedelta
import time

def generate_game_data(num_players=100, games_per_player=25):
    """Generate sample game data for the Cosmic Defenders game."""
    
    game_modes = ["battle-royale", "team-deathmatch", "capture-the-flag", "survival"]
    achievements = [
        "FirstBlood", "DoubleKill", "TripleKill", "QuadraKill", "PentaKill",
        "Headshot", "Survivor", "MVP", "TeamPlayer", "Defender", "Attacker"
    ]
    
    # Generate player names
    adjectives = ["Cosmic", "Galactic", "Stellar", "Astral", "Nebula", "Solar", "Lunar", "Quantum"]
    nouns = ["Warrior", "Hunter", "Defender", "Ranger", "Knight", "Sniper", "Pilot", "Commander"]
    
    game_data = []
    
    # Current time for reference
    now = datetime.now()
    
    # Generate data for each player
    for i in range(num_players):
        player_id = f"p{uuid.uuid4().hex[:8]}"
        player_name = f"{random.choice(adjectives)}{random.choice(nouns)}{random.randint(1, 999)}"
        
        # Generate multiple games for each player
        for j in range(games_per_player):
            # Random date within the last 30 days
            days_ago = random.randint(0, 30)
            game_date = (now - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            
            # Random time on that day
            hours = random.randint(0, 23)
            minutes = random.randint(0, 59)
            seconds = random.randint(0, 59)
            timestamp = f"{game_date}T{hours:02d}:{minutes:02d}:{seconds:02d}Z"
            
            game_id = f"g{uuid.uuid4().hex[:8]}"
            score = random.randint(1000, 10000)
            game_duration = random.randint(180, 900)  # 3-15 minutes in seconds
            
            # Random number of achievements (0-3)
            num_achievements = random.randint(0, 3)
            game_achievements = random.sample(achievements, num_achievements)
            
            # TTL - set some records to expire in the future (for TTL demo)
            # 30% of records will have an expiration time
            if random.random() < 0.3:
                # Expire in 1-30 days from now
                expire_days = random.randint(1, 30)
                expiration_time = int((now + timedelta(days=expire_days)).timestamp())
            else:
                expiration_time = 0  # No expiration
            
            # Create game record
            game_record = {
                "player_id": player_id,
                "game_id": game_id,
                "player_name": player_name,
                "game_date": game_date,
                "score": score,
                "game_duration": game_duration,
                "achievements": game_achievements,
                "game_mode": random.choice(game_modes),
                "expiration_time": expiration_time,
                "last_updated": timestamp
            }
            
            game_data.append(game_record)
    
    # Shuffle the data to mix players and dates
    random.shuffle(game_data)
    
    return game_data

if __name__ == "__main__":
    # Generate data for 50 players with 10 games each (500 total records)
    game_data = generate_game_data(80, 25)
    
    # Save to JSON file
    with open("game_data.json", "w") as f:
        json.dump(game_data, f, indent=2)
    
    print(f"Generated {len(game_data)} game records and saved to game_data.json")
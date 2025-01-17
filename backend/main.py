from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import json
import random
import time
from typing import Dict, List

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

clients: Dict[WebSocket, dict] = {}

CHALLENGES = [
    {
        "id": 1,
        "title": "The Quest Begins",
        "description": "Write a function that returns your hero's battle cry! Make it inspiring!",
        "template": "def battle_cry():\n    # Write your hero's battle cry\n    return 'For glory!'",
        "test_cases": [{"input": [], "expected_type": "str"}],
        "xp": 100,
        "level": "Beginner",
        "hints": [
            "A function returns a value using the 'return' keyword",
            "Strings in Python are wrapped in quotes, like 'Hello' or \"Hello\"",
            "Try making your battle cry personal and unique!"
        ],
        "example": "def battle_cry():\n    return 'For honor and glory!'",
        "explanation": "This function uses the 'return' keyword to send back a string (text) that represents your hero's battle cry."
    },
    {
        "id": 2,
        "title": "Dragon's Math",
        "description": "The dragon demands a solution! Write a function that calculates the sum of all numbers from 1 to n.",
        "template": "def dragon_sum(n):\n    # Calculate the sum of numbers from 1 to n\n    pass",
        "test_cases": [
            {"input": [5], "expected": 15},
            {"input": [10], "expected": 55}
        ],
        "xp": 150,
        "level": "Adventurer",
        "hints": [
            "You can use a for loop to go through numbers: 'for i in range(1, n+1)'",
            "Keep track of the sum in a variable",
            "The formula n * (n + 1) / 2 can also solve this!",
            "Don't forget to return the final sum"
        ],
        "example": "def dragon_sum(n):\n    total = 0\n    for i in range(1, n + 1):\n        total += i\n    return total",
        "explanation": "This function uses a loop to add up all numbers from 1 to n. The variable 'total' keeps track of the sum as we go."
    },
    {
        "id": 3,
        "title": "Magical Palindrome",
        "description": "Cast a spell to check if a word is the same forwards and backwards!",
        "template": "def is_magical_word(word):\n    # Check if the word is a palindrome\n    pass",
        "test_cases": [
            {"input": ["radar"], "expected": True},
            {"input": ["magic"], "expected": False}
        ],
        "xp": 200,
        "level": "Wizard",
        "hints": [
            "You can reverse a string in Python using slice notation: word[::-1]",
            "Compare the original word with its reverse",
            "Remember that True/False values don't need quotes",
            "You can also loop through the string and compare characters from both ends"
        ],
        "example": "def is_magical_word(word):\n    return word == word[::-1]",
        "explanation": "This function checks if a word is a palindrome by comparing it with its reverse. The [::-1] slice notation creates a reversed copy of the string."
    }
]

ACHIEVEMENTS = {
    "first_code": {"name": "First Quest Complete!", "xp": 50},
    "speed_demon": {"name": "Speed Demon", "xp": 100},
    "perfect_code": {"name": "Perfect Code", "xp": 150},
    "hint_master": {"name": "Knowledge Seeker", "xp": 25}
}

@app.get("/")
async def read_root():
    return {"message": "Code Quest API - Your Coding Adventure Awaits!"}

@app.get("/challenges")
async def get_challenges():
    return CHALLENGES

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients[websocket] = {
        "score": 0,
        "completed_challenges": set(),
        "achievements": set(),
        "hints_used": set()
    }
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "code_submission":
                start_time = time.time()
                challenge_id = message["challengeId"]
                code = message["code"]
                
                challenge = next((c for c in CHALLENGES if c["id"] == challenge_id), None)
                if not challenge:
                    continue

                execution_time = random.uniform(0.1, 0.5)
                time.sleep(execution_time)
                
                success = random.random() > 0.3
                output = "Your code runs like magic!" if success else "The spell fizzled... Try using the hints for guidance!"
                
                rewards = []
                if success:
                    xp_gained = challenge["xp"]
                    
                    if execution_time < 0.2:
                        xp_gained += 50
                        if "speed_demon" not in clients[websocket]["achievements"]:
                            clients[websocket]["achievements"].add("speed_demon")
                            rewards.append(ACHIEVEMENTS["speed_demon"])
                    
                    if challenge_id not in clients[websocket]["completed_challenges"]:
                        clients[websocket]["completed_challenges"].add(challenge_id)
                        if len(clients[websocket]["completed_challenges"]) == 1:
                            clients[websocket]["achievements"].add("first_code")
                            rewards.append(ACHIEVEMENTS["first_code"])
                    
                    clients[websocket]["score"] += xp_gained
                
                response = {
                    "type": "result",
                    "success": success,
                    "output": output,
                    "executionTime": execution_time,
                    "xpGained": xp_gained if success else 0,
                    "totalXp": clients[websocket]["score"],
                    "rewards": rewards
                }
                
                await websocket.send_json(response)
            
            elif message["type"] == "get_stats":
                stats = {
                    "type": "stats",
                    "score": clients[websocket]["score"],
                    "completedChallenges": len(clients[websocket]["completed_challenges"]),
                    "achievements": [ACHIEVEMENTS[a] for a in clients[websocket]["achievements"]]
                }
                await websocket.send_json(stats)
            
            elif message["type"] == "request_hint":
                challenge_id = message["challengeId"]
                hint_key = f"{challenge_id}_hint"
                
                if hint_key not in clients[websocket]["hints_used"]:
                    clients[websocket]["hints_used"].add(hint_key)
                    clients[websocket]["achievements"].add("hint_master")
                    clients[websocket]["score"] += ACHIEVEMENTS["hint_master"]["xp"]
                    
                    response = {
                        "type": "hint_reward",
                        "achievement": ACHIEVEMENTS["hint_master"],
                        "totalXp": clients[websocket]["score"]
                    }
                    await websocket.send_json(response)
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        del clients[websocket]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import json
import time
from typing import Dict, List
import ast
import sys
from io import StringIO
from contextlib import redirect_stdout

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

def is_safe_code(code: str) -> bool:
    """Check if the code is safe to execute."""
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            # Prevent imports, file operations, and system calls
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                return False
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ['eval', 'exec', 'open', 'system']:
                        return False
        return True
    except:
        return False

def run_code_safely(code: str, test_cases: List[dict]) -> tuple:
    """Run code safely and return output and success status."""
    if not is_safe_code(code):
        return "Code contains unsafe operations!", False

    # Capture stdout
    output_buffer = StringIO()
    
    try:
        # Create a new namespace for the code
        namespace = {}
        
        # Execute the code in the namespace
        with redirect_stdout(output_buffer):
            exec(code, namespace)
        
        # Run test cases
        for test_case in test_cases:
            func_name = code.split('def ')[1].split('(')[0].strip()
            if func_name not in namespace:
                return f"Function {func_name} not found!", False
            
            func = namespace[func_name]
            result = func(*test_case.get('input', []))
            
            if 'expected_type' in test_case:
                if not isinstance(result, eval(test_case['expected_type'])):
                    return f"Expected return type {test_case['expected_type']}, got {type(result).__name__}", False
            elif 'expected' in test_case:
                if result != test_case['expected']:
                    return f"Test failed! Expected {test_case['expected']}, got {result}", False
        
        output = output_buffer.getvalue()
        return output or "Code ran successfully!", True
        
    except Exception as e:
        return f"Error: {str(e)}", False

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

                output, success = run_code_safely(code, challenge["test_cases"])
                execution_time = time.time() - start_time
                
                rewards = []
                xp_gained = 0
                
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
                    "xpGained": xp_gained,
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

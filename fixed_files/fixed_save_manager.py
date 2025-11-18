import os
import json

SAVE_FILE = "saves/current.json"

def save_game_state(state):
    os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
    try:
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
        print("game saved")
    except (IOError, OSError) as e:
        print(f"save failed: {e}")

def load_game_state():
    if not os.path.exists(SAVE_FILE):
        print("no save file")
        return None
    try:
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (IOError, OSError, json.JSONDecodeError) as e:
        print(f"load failed: {e}")
        return None
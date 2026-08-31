import json
import re

with open("yt_game.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def find_keys(node, kw):
    if isinstance(node, dict):
        for k, v in node.items():
            if kw.lower() in str(v).lower():
                print(f"Key: {k} -> {str(v)[:200]}")
            find_keys(v, kw)
    elif isinstance(node, list):
        for item in node:
            find_keys(item, kw)

print("--- Searching for SayGames ---")
find_keys(data, "SayGames")

print("\n--- Searching for Description ---")
find_keys(data, "Become a ninja") # Just guessing a description keyword, or I can search for something like "description"

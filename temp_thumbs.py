import json

with open("yt_game.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def find_thumbs(node):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == 'thumbnails' and isinstance(v, list):
                print("Found thumbnails list:")
                for t in v:
                    print("  - ", t.get('width', '?'), "x", t.get('height', '?'), t.get('url', '?')[:100])
            find_thumbs(v)
    elif isinstance(node, list):
        for item in node:
            find_thumbs(item)

find_thumbs(data)

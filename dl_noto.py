import re
import urllib.request
import os

emoji_map = {
    'action': ['💥', '💣', '🔥', '🥊', '🔫'],
    'romance': ['💖', '🥰', '💘', '💍', '🌹'],
    'comedy': ['😂', '🤣', '🤪', '🤡', '😆'],
    'historical': ['⛩️', '🗡️', '🏯', '📜'],
    'psychological': ['🧠', '😵‍💫', '🎭', '🌀', '👁️'],
    'crime': ['🕵️', '🚓', '🩸', '🔪', '🔍'],
    'scifi': ['🚀', '👽', '🤖', '🛸', '🌌'],
    'horror': ['👻', '💀', '🧟', '🎃', '🧛'],
    'animation': ['🦄', '🌈', '🧸', '🎈', '🪄'],
    'lgbt': ['🏳️‍🌈', '👨‍❤️‍👨', '👩‍❤️‍👩', '👬', '👭'],
    'party': ['🎉', '🎊', '🥂', '🥳', '🎁'],
    'cry': ['😭', '💔', '🥀', '☔', '😢'],
    'rage': ['🤬', '🌋', '💢', '😠'],
    'chill': ['🍿', '🥤', '🛋️', '☕', '🎧'],
    'tense': ['😱', '😰', '🥶', '👀', '⏳'],
}

def get_hex(char):
    codepoints = [hex(ord(c))[2:] for c in char if ord(c) != 0xFE0F]
    return "_".join(codepoints)

os.makedirs("assets/lottie", exist_ok=True)
downloaded_assets = {}

for category, emojis in emoji_map.items():
    downloaded_assets[category] = []
    for e in emojis:
        hx = get_hex(e)
        base_hx = hex(ord(e[0]))[2:]
        url = f"https://fonts.gstatic.com/s/e/notoemoji/latest/{hx}/lottie.json"
        
        file_path = f"assets/lottie/noto_{hx}.json"
        
        if not os.path.exists(file_path):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    with open(file_path, 'wb') as out_file:
                        out_file.write(response.read())
                downloaded_assets[category].append(file_path)
            except Exception:
                # Try base
                url2 = f"https://fonts.gstatic.com/s/e/notoemoji/latest/{base_hx}/lottie.json"
                file_path2 = f"assets/lottie/noto_{base_hx}.json"
                if not os.path.exists(file_path2):
                    try:
                        req = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req, timeout=5) as response:
                            with open(file_path2, 'wb') as out_file:
                                out_file.write(response.read())
                        downloaded_assets[category].append(file_path2)
                    except:
                        pass
                else:
                    downloaded_assets[category].append(file_path2)
        else:
            downloaded_assets[category].append(file_path)

# Update next_episode_tracker.dart
with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    text = f.read()

for category, paths in downloaded_assets.items():
    if not paths: continue
    
    # We will append these paths to the arrays in the dart file.
    # Find the array for the category.
    # SupportedGenre.action: ['assets/lottie/lf20_fyye8szy.json', '💥', '💣', '🔥', '🥊', '🏍️', '🔫'],
    
    # We'll just replace the whole emoji strings with the lottie paths for this category
    paths_str = ", ".join([f"'{p}'" for p in paths])
    
    if category in ['party','cry','rage','chill','tense']:
        # progress
        pattern = r"'" + category + r"':\s*\[(.*?)\]"
        match = re.search(pattern, text)
        if match:
            existing = match.group(1)
            # Combine existing json with new noto jsons, remove raw emojis
            existing_jsons = [x.strip() for x in existing.split(",") if ".json" in x]
            all_jsons = existing_jsons + [f"'{p}'" for p in paths]
            new_val = "'" + category + "': [" + ", ".join(all_jsons) + "]"
            text = text.replace(match.group(0), new_val)
    else:
        # genre
        pattern = r"SupportedGenre\." + category + r":\s*\[(.*?)\]"
        match = re.search(pattern, text)
        if match:
            existing = match.group(1)
            existing_jsons = [x.strip() for x in existing.split(",") if ".json" in x]
            all_jsons = existing_jsons + [f"'{p}'" for p in paths]
            new_val = "SupportedGenre." + category + ": [" + ", ".join(all_jsons) + "]"
            text = text.replace(match.group(0), new_val)

with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(text)

print("Downloaded Noto Lotties and updated dart file!")

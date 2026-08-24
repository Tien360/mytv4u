import re
import urllib.request

emoji_map = {
    'action': ['💥', '💣', '🔥', '🥊', '🏍️', '🔫'],
    'romance': ['💖', '🥰', '💘', '💍', '💏', '🌹'],
    'comedy': ['😂', '🤣', '🤪', '🤡', '😆', '🙊'],
    'historical': ['⛩️', '🗡️', '🏯', '📜', '🎎'],
    'psychological': ['🧠', '😵‍💫', '🎭', '🌀', '👁️'],
    'crime': ['🕵️', '🚓', '🩸', '🔪', '🔍'],
    'scifi': ['🚀', '👽', '🤖', '🛸', '🌌'],
    'horror': ['👻', '💀', '🧟', '🎃', '🧛', '🔪'],
    'animation': ['🦄', '🌈', '🧸', '🎈', '🪄'],
    'lgbt': ['🏳️‍🌈', '👨‍❤️‍👨', '👩‍❤️‍👩', '👬', '👭'],
    'party': ['🎉', '🎊', '🥂', '🥳', '🎁', '💃'],
    'cry': ['😭', '💔', '🥀', '☔', '😢'],
    'rage': ['🤬', '🌋', '💢', '😠'],
    'chill': ['🍿', '🥤', '🛋️', '☕', '🎧', '🧘'],
    'tense': ['😱', '😰', '🥶', '👀', '⏳'],
}

def get_hex(char):
    # Get the hex code of the first codepoint (some have modifiers, we take the base usually or try both)
    # Actually, Noto usually expects the exact hex string, e.g. 1f602
    codepoints = [hex(ord(c))[2:] for c in char if ord(c) != 0xFE0F] # strip variation selector
    return "_".join(codepoints)

valid_lotties = {}
for category, emojis in emoji_map.items():
    valid_lotties[category] = []
    for e in emojis:
        hx = get_hex(e)
        url = f"https://fonts.gstatic.com/s/e/notoemoji/latest/{hx}/lottie.json"
        try:
            req = urllib.request.Request(url, method="HEAD")
            resp = urllib.request.urlopen(req, timeout=3)
            if resp.status == 200:
                valid_lotties[category].append(url)
                print(f"OK: {e} -> {url}")
        except Exception:
            # Fallback to single base codepoint if multi-codepoint failed
            base_hx = hex(ord(e[0]))[2:]
            url = f"https://fonts.gstatic.com/s/e/notoemoji/latest/{base_hx}/lottie.json"
            try:
                req = urllib.request.Request(url, method="HEAD")
                resp = urllib.request.urlopen(req, timeout=3)
                if resp.status == 200:
                    valid_lotties[category].append(url)
                    print(f"OK (Base): {e} -> {url}")
                else:
                    print(f"Fail: {e}")
            except:
                print(f"Fail: {e}")

# Now generate Dart code snippets to inject
dart_genre = ""
for k, v in valid_lotties.items():
    if k in ['party','cry','rage','chill','tense']: continue
    urls = ", ".join([f"'{u}'" for u in v])
    print(f"SupportedGenre.{k}: [{urls}],")


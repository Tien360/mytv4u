import re

def fix_fallback_await(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the specific await in _tryFallbackDomain
    pattern = r"(bool _tryFallbackDomain\(\) \{[\s\S]*?)await (player\.open\(Media\(newUrl\)\);[\s\S]*?return false;\n  \})"
    
    # We replace 'await ' with '' in that specific block
    content = re.sub(pattern, r"\1\2", content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_fallback_await('lib/screens/player_screen.dart')
print("Fixed await in synchronous function using regex")

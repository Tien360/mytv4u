import sys
with open('lib/screens/game_detail_screen.dart', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace currentThumb with widget.initialThumb for the Hero poster
target_hero = """                          child: Image.network(
                            currentThumb,
                            width: 300,
                            height: 300,
                            fit: BoxFit.cover,"""
new_hero = """                          child: Image.network(
                            widget.initialThumb,
                            width: 300,
                            height: 300,
                            fit: BoxFit.cover,"""

if target_hero in c:
    c = c.replace(target_hero, new_hero)
    with open('lib/screens/game_detail_screen.dart', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Fixed Hero poster to use initialThumb")
else:
    print("Could not find target_hero")


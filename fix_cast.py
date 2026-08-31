def fix_cast(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace("player.platform?.setProperty", "(player.platform as dynamic).setProperty")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_cast('lib/screens/player_screen.dart')
print("Fixed setProperty cast")

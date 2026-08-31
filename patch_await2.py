def add_await_to_player_open2(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the player.open call in fallback
    target = "player.open(Media(newUrl));"
    replacement = "await player.open(Media(newUrl));"
    
    content = content.replace(target, replacement)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

add_await_to_player_open2('lib/screens/player_screen.dart')
print("Added await to player.open in fallback")

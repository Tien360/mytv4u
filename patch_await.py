def add_await_to_player_open(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the player.open call in _playCurrentUrl
    target = "player.open(Media(_currentUrl, httpHeaders: headers), play: false);"
    replacement = "await player.open(Media(_currentUrl, httpHeaders: headers), play: false);"
    
    content = content.replace(target, replacement)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

add_await_to_player_open('lib/screens/player_screen.dart')
print("Added await to player.open")

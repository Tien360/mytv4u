def remove_4k_cap(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace("width: 3840, height: 2160, \n        ", "")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

remove_4k_cap('lib/screens/tv_player_screen.dart')
print("Removed 4K cap from tv_player_screen")

import io

def fix_file(path):
    with io.open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    text = text.replace("title.contains('l?ng ti?ng')", "title.contains('lồng tiếng')")
    text = text.replace("title.contains('thuy?t minh')", "title.contains('thuyết minh')")

    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(text)

fix_file(r'lib\screens\player_screen.dart')
fix_file(r'lib\screens\tv_player_screen.dart')

import re

def add_lavc_threads(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r"platform\.setProperty\('demuxer-lavf-o-append', 'fflags\+fastseek'\);"
    
    replacement = r"platform.setProperty('demuxer-lavf-o-append', 'fflags=+fastseek');\n      platform.setProperty('vd-lavc-threads', '16'); // 16 luong CPU gank 8K neu hwdec that bai"
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

add_lavc_threads('lib/screens/player_screen.dart')
add_lavc_threads('lib/screens/tv_player_screen.dart')
print("Patched lavc threads")

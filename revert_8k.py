import re

def revert_8k_props(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r"// Tối ưu 8K / HLS.*?platform\.setProperty\('framedrop', 'decoder'\); // Cho phép rớt frame để chống đứng máy khi tải quá nặng"
    content = re.sub(pattern, "", content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

revert_8k_props('lib/screens/player_screen.dart')
revert_8k_props('lib/screens/tv_player_screen.dart')
print("Reverted 8K props")

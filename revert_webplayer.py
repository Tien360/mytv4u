import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the button
pattern_btn = r"(\s*)if \(_isYoutube && _ytQualities\.any\(\(q\) => q >= 2160\)\) \.\.\.\[[\s\S]*?\](,)?\s*(?=(// Settings Gear Button))"
content = re.sub(pattern_btn, r"\1\3", content)

# Remove the function _openInWebPlayer
pattern_func = r"(\s*)void _openInWebPlayer\(\) async \{[\s\S]*?catch \(e\) \{\s*debugPrint\('Error launching web player: \$e'\);\s*\}\s*\}"
content = re.sub(pattern_func, "", content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Reverted Web Player feature")

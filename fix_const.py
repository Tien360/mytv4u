path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\library_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Replace `const Text(\n                          L10n.t` with `Text(\n                          L10n.t`
text = re.sub(r'const\s+Text\(\s*L10n\.t', 'Text(L10n.t', text)

# Also check for other const wrappers like const Dialog or const Column? 
# The errors were:
# line 93, 117 (which are the const Text above)
# line 312:
# line 353:

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print("Removed consts from Text(L10n...)")

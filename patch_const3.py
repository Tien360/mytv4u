path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# find line with "const SnackBar(" near line 1460
for i, line in enumerate(lines):
    if "const SnackBar(" in line and "yt_login_success" in "".join(lines[i:i+3]):
        lines[i] = line.replace("const SnackBar(", "SnackBar(")
    if "const Row(" in line and "yt_login_browser_title" in "".join(lines[i:i+5]):
        lines[i] = line.replace("const Row(", "Row(")
    if "const Text(L10n.t('yt_login_browser_success')" in line:
        lines[i] = line.replace("const Text(", "Text(")

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Removed consts")

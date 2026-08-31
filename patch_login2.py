path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("Navigator.of(context, rootNavigator: true).pop();", "Navigator.of(context, rootNavigator: true).pop();\n             SharedPreferences.getInstance().then((p) { p.setBool('is_yt_linked', true); setState(() => _isYtLinked = true); });")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated successful login block again")

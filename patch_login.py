path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

target = "             Navigator.of(context, rootNavigator: true).pop();\n             ScaffoldMessenger.of(context).showSnackBar("
new_target = "             Navigator.of(context, rootNavigator: true).pop();\n             SharedPreferences.getInstance().then((prefs) {\n               prefs.setBool('is_yt_linked', true);\n               setState(() => _isYtLinked = true);\n             });\n             ScaffoldMessenger.of(context).showSnackBar("

content = content.replace(target, new_target)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated successful login block")

import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\library_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure SharedPreferences is imported
if "shared_preferences.dart" not in content:
    content = content.replace("import 'package:flutter/material.dart';", "import 'package:flutter/material.dart';\nimport 'package:shared_preferences/shared_preferences.dart';")

search = """final res = await Process.run(exePath, ['--dump-json', '--flat-playlist', url]);"""
new_code = """
                              final prefs = await SharedPreferences.getInstance();
                              final cookieSource = prefs.getString('yt_cookie_source') ?? 'none';
                              List<String> args = ['--dump-json', '--flat-playlist', url];
                              if (cookieSource != 'none') {
                                args.insert(0, cookieSource);
                                args.insert(0, '--cookies-from-browser');
                              }
                              final res = await Process.run(exePath, args);"""

if search in content:
    content = content.replace(search, new_code)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched library_screen.dart")
else:
    print("Could not find search string in library_screen.dart")

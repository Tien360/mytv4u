import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\library_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add path_provider and path imports
imports = "import 'package:path_provider/path_provider.dart';\nimport 'package:path/path.dart' as p;"
if "path_provider" not in content:
    content = content.replace("import 'package:shared_preferences/shared_preferences.dart';", "import 'package:shared_preferences/shared_preferences.dart';\n" + imports)

search = """                              if (cookieSource != 'none') {
                                args.insert(0, cookieSource);
                                args.insert(0, '--cookies-from-browser');
                              }"""

new_code = """                              if (cookieSource != 'none') {
                                if (cookieSource == 'webview') {
                                  final appDataDir = await getApplicationSupportDirectory();
                                  final ebPath = p.join(appDataDir.path, 'youtube_webview_profile', 'EBWebView');
                                  args.insert(0, 'edge:$ebPath');
                                  args.insert(0, '--cookies-from-browser');
                                } else {
                                  args.insert(0, cookieSource);
                                  args.insert(0, '--cookies-from-browser');
                                }
                              }"""

content = content.replace(search, new_code)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

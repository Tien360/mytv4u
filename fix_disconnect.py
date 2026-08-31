import re

def patch_settings(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add dart:io
    content = "import 'dart:io';\n" + content

    # Find the disconnect block
    old_disconnect = r"await prefs\.setBool\('is_yt_linked', false\);\s*setState\(\(\) => _isYtLinked = false\);"
    
    new_disconnect = '''await prefs.setBool('is_yt_linked', false);
                    setState(() => _isYtLinked = false);
                    
                    try {
                      final exeName = File(Platform.resolvedExecutable).uri.pathSegments.last.replaceAll('.exe', '');
                      final defaultWebviewPath = '\\\\flutter_webview_windows\\\\\\\\EBWebView';
                      final dir = Directory(defaultWebviewPath);
                      if (dir.existsSync()) {
                        dir.deleteSync(recursive: true);
                      }
                    } catch (e) {
                      debugPrint('Failed to delete WebView data: \');
                    }'''
        
    match = re.search(old_disconnect, content, flags=re.MULTILINE)
    if match:
        content = content.replace(match.group(0), new_disconnect)
    else:
        print("Could not find disconnect block in settings_screen")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_settings('lib/screens/settings_screen.dart')
print("Patched settings_screen.dart disconnect logic")

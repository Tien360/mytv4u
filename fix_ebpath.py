import re

def patch(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the block where we set ebPath
    old_block = r"final appDataDir = await getApplicationSupportDirectory\(\);\s*final ebPath = appDataDir\.path \+ '\\\\youtube_webview_profile\\\\EBWebView';"
    
    new_block = '''final localAppData = Platform.environment['LOCALAPPDATA'];
        final exeName = File(Platform.resolvedExecutable).uri.pathSegments.last.replaceAll('.exe', '');
        final defaultWebviewPath = '\\\\\flutter_webview_windows\\\\\\\\\EBWebView';
        final appDataDir = await getApplicationSupportDirectory();
        final customWebviewPath = '\\\\\youtube_webview_profile\\\\EBWebView';
        
        String ebPath = defaultWebviewPath;
        if (Directory(customWebviewPath).existsSync()) {
          ebPath = customWebviewPath;
        }'''
        
    match = re.search(old_block, content, flags=re.MULTILINE)
    if match:
        content = content.replace(match.group(0), new_block)
    else:
        print("Could not find old block in player_screen")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch('lib/screens/player_screen.dart')
print("Patched player_screen.dart with smart cookie path")

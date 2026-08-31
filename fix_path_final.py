import re

def fix_path(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_block = r"final exeName = File\(Platform\.resolvedExecutable\)\.uri\.pathSegments\.last\.replaceAll\('\.exe', ''\);\s*final defaultWebviewPath = '[^']*';\s*final appDataDir = await getApplicationSupportDirectory\(\);\s*final customWebviewPath = '\$\{appDataDir\.path\}\\\\youtube_webview_profile\\\\EBWebView';"
    
    new_block = '''final exeName = File(Platform.resolvedExecutable).uri.pathSegments.last.replaceAll('.exe', '');
        final defaultWebviewPath = '${Platform.environment['LOCALAPPDATA']}\\\\flutter_webview_windows\\\\${exeName}\\\\EBWebView';
        final appDataDir = await getApplicationSupportDirectory();
        final customWebviewPath = '${appDataDir.path}\\\\youtube_webview_profile\\\\EBWebView';'''
        
    match = re.search(old_block, content, flags=re.MULTILINE)
    if match:
        content = content.replace(match.group(0), new_block)
    else:
        print("Could not find block in " + filepath)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_path('lib/screens/player_screen.dart')
fix_path('lib/screens/library_screen.dart')
print("Fixed defaultWebviewPath properly")

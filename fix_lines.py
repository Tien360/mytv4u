def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        if "final defaultWebviewPath =" in line:
            lines[i] = "        final defaultWebviewPath = '${Platform.environment['LOCALAPPDATA']}\\\\flutter_webview_windows\\\\${exeName}\\\\EBWebView';\n"
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)

fix_file('lib/screens/player_screen.dart')
fix_file('lib/screens/library_screen.dart')
print("Fixed lines directly")

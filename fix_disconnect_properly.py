def patch_settings(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_disconnect = r"final exeName = File(Platform.resolvedExecutable).uri.pathSegments.last.replaceAll('.exe', '');\n                      final defaultWebviewPath = '\\flutter_webview_windows\\\\EBWebView';"
    
    new_disconnect = '''final exeName = File(Platform.resolvedExecutable).uri.pathSegments.last.replaceAll('.exe', '');
                      final defaultWebviewPath = '${Platform.environment['LOCALAPPDATA']}\\\\flutter_webview_windows\\\\${exeName}\\\\EBWebView';'''
        
    content = content.replace(old_disconnect, new_disconnect)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_settings('lib/screens/settings_screen.dart')
print("Patched settings_screen.dart disconnect logic correctly")

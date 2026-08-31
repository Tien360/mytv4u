def patch_settings(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the bad line
    content = content.replace("final defaultWebviewPath = '${Platform.environment['LOCALAPPDATA']}\\flutter_webview_windows\\${exeName}\\EBWebView';",
                              "final defaultWebviewPath = '${Platform.environment['LOCALAPPDATA']}\\\\flutter_webview_windows\\\\${exeName}\\\\EBWebView';")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_settings('lib/screens/settings_screen.dart')
print("Patched double backslashes correctly")

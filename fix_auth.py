def fix_auth(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the bad line
    content = content.replace("onPressed: _login,", "onPressed: _handleLogin,")
    content = content.replace("await AuthApi.logout();\n                    setState(() => _currentUser = null);", "await _handleLogout();")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_auth('lib/screens/settings_screen.dart')
print("Patched auth methods correctly")

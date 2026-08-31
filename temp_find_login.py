with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("Widget _buildLoginCard")
if idx != -1:
    print(content[idx:idx+1500])

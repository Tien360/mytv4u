def fix_yt_ui(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    target_ui = '''if (_isYoutubeLink) ...['''
    replacement_ui = '''if (_isYoutubeLink && _ytQualities.isNotEmpty) ...['''
    content = content.replace(target_ui, replacement_ui)

    target_val = '''value: _selectedYtQuality,'''
    replacement_val = '''value: _ytQualities.contains(_selectedYtQuality) ? _selectedYtQuality : _ytQualities.first,'''
    content = content.replace(target_val, replacement_val)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_yt_ui('lib/screens/player_screen.dart')
print("Fixed YouTube UI crash condition")

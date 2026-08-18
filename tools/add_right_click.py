import sys

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

old_code = '''        child: MouseRegion(
          onHover: (_) => _onHoverOrTap(),
          child: GestureDetector(
            onTap: _onHoverOrTap,
            child: Stack('''
new_code = '''        child: MouseRegion(
          onHover: (_) => _onHoverOrTap(),
          child: GestureDetector(
            onTap: _onHoverOrTap,
            onSecondaryTap: _showSettingsDialog,
            child: Stack('''
text = text.replace(old_code, new_code)

with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

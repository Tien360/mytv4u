files = [
    'lib/screens/splash_screen.dart',
    'lib/screens/tv_screen.dart',
    'lib/screens/tv_webview_screen.dart',
    'lib/widgets/update_dialog.dart'
]

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'l10n.dart' not in content:
        import_str = "import '../utils/l10n.dart';"
        content = content.replace('import ', import_str + '\nimport ', 1)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

print('Added imports')

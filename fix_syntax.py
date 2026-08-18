with open('lib/widgets/advanced_controls_panel.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('              ),\n      ),\n    );\n  }', '              ),\n    );\n  }')

with open('lib/widgets/advanced_controls_panel.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print('Syntax fixed')

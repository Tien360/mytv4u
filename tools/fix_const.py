
with open('lib/widgets/update_dialog.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('child: const Row(', 'child: Row(')

with open('lib/widgets/update_dialog.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed const')


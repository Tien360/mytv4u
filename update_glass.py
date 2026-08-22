
with open('lib/widgets/glass_container.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('this.color = const Color(0x0CFFFFFF)', 'this.color = const Color(0x1AFFFFFF)')
content = content.replace('this.borderColor = const Color(0x1AFFFFFF)', 'this.borderColor = const Color(0x33FFFFFF)')
content = content.replace('this.blur = 20.0', 'this.blur = 30.0')

with open('lib/widgets/glass_container.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated glass container')


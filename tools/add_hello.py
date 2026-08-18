import sys

with open('assets/langs/en.json', 'r', encoding='utf-8') as f:
    text = f.read()
text = text.replace('}', ',\n  "hello": "Hello"\n}')
with open('assets/langs/en.json', 'w', encoding='utf-8') as f:
    f.write(text)

with open('assets/langs/vi.json', 'r', encoding='utf-8') as f:
    text = f.read()
text = text.replace('}', ',\n  "hello": "Xin chào"\n}')
with open('assets/langs/vi.json', 'w', encoding='utf-8') as f:
    f.write(text)

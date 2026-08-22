with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

pos = 38892
print(text[pos-100:pos+100])

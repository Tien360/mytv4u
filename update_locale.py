import re

with open('lib/widgets/glass_search_bar.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace _speech.listen with localeId
listen_code = '''
        String locale = L10n.currentLang == 'vi' ? 'vi_VN' : 'en_US';
        _speech.listen(
          localeId: locale,
          onResult: (val) => setState(() {
'''

content = re.sub(
    r'_speech\.listen\(\s*onResult:\s*\(val\)\s*=>\s*setState\(\(\)\s*\{',
    listen_code,
    content
)

with open('lib/widgets/glass_search_bar.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print('Added localeId to speech_to_text')

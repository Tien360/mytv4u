
with open('pubspec.yaml', 'r', encoding='utf-8') as f:
    if 'speech_to_text' in f.read():
        print('speech_to_text is installed')
    else:
        print('speech_to_text is NOT installed')


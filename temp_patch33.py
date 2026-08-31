with open('all_settings_replacements.txt', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find("                                  SizedBox(key: _videoKey),")
end_idx = text.find("                                  SizedBox(key: _colorKey),")
if start_idx != -1 and end_idx != -1:
    video_block = text[start_idx:end_idx]
    
    with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as sf:
        settings_text = sf.read()
        
    rep_start = settings_text.find("                                  SizedBox(key: _videoKey),")
    rep_end = settings_text.find("                                  SizedBox(key: _colorKey),")
    if rep_start != -1 and rep_end != -1:
        settings_text = settings_text[:rep_start] + video_block + settings_text[rep_end:]
        with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as sf:
            sf.write(settings_text)
        print("Injected Video Block perfectly!")
    else:
        print("Could not find video block in settings_screen.dart")
else:
    print("Could not find video block in backups!")

import sys
with open('temp_patch7.py', 'r', encoding='utf-8') as f:
    text = f.read()
    
start_v = text.find('video_block = """') + len('video_block = """')
end_v = text.find('"""\n\nif "T?c')
video_block = text[start_v:end_v]

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

rep_idx = content.find("                                            _syncToFirebase();\n                                          },\n                                        ),\n                                      ],\n                                    ),\n                                  ),")

if rep_idx != -1:
    rep_idx += len("                                            _syncToFirebase();\n                                          },\n                                        ),\n                                      ],\n                                    ),\n                                  ),")
    content = content[:rep_idx] + "\n" + video_block + content[rep_idx:]
    with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected video block via index!")
else:
    print("Could not find injection point")

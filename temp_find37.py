import sys

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

search_str = "                                                  _syncToFirebase();\n                                                }\n                                              },\n                                            ),\n                                          ),"

idx = content.find(search_str)
if idx != -1:
    print(repr(content[idx:idx+300]))
else:
    print("Could not find default_speed block!")

import re
content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

if 'firebase_api.dart' not in content:
    content = content.replace("import 'package:shared_preferences/shared_preferences.dart';", "import 'package:shared_preferences/shared_preferences.dart';\nimport '../api/firebase_api.dart';")

content = content.replace("prefs.setString('audio_visualizer', val);\n                                    setDialogState", "prefs.setString('audio_visualizer', val);\n                                    FirebaseApi.saveUserSettings({'audio_visualizer': val});\n                                    setDialogState")

content = content.replace("prefs.setBool('audio_vinyl', val);\n                                  setDialogState", "prefs.setBool('audio_vinyl', val);\n                                  FirebaseApi.saveUserSettings({'audio_vinyl': val});\n                                  setDialogState")

content = content.replace("prefs.setInt('audio_sleep_timer', val);\n                                    setDialogState", "prefs.setInt('audio_sleep_timer', val);\n                                    FirebaseApi.saveUserSettings({'audio_sleep_timer': val});\n                                    setDialogState")

open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)

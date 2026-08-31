import re

content = open('lib/widgets/optimizer_dialog.dart', 'r', encoding='utf-8').read()

if "'audio_visualizer':" not in content:
    content = content.replace("'enable_easter_eggs': prefs.getBool('enable_easter_eggs') ?? true,", "'enable_easter_eggs': prefs.getBool('enable_easter_eggs') ?? true,\n      'audio_visualizer': prefs.getString('audio_visualizer') ?? 'bars',\n      'audio_vinyl': prefs.getBool('audio_vinyl') ?? true,")
    content = content.replace("await prefs.setBool('enable_easter_eggs', backup['enable_easter_eggs'] ?? true);", "await prefs.setBool('enable_easter_eggs', backup['enable_easter_eggs'] ?? true);\n      \n      if (backup.containsKey('audio_visualizer')) {\n        await prefs.setString('audio_visualizer', backup['audio_visualizer']);\n      }\n      if (backup.containsKey('audio_vinyl')) {\n        await prefs.setBool('audio_vinyl', backup['audio_vinyl']);\n      }")

open('lib/widgets/optimizer_dialog.dart', 'w', encoding='utf-8').write(content)
print("Patched optimizer_dialog backups!")

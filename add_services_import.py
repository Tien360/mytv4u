import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()
if 'package:flutter/services.dart' not in content:
    content = content.replace("import 'package:flutter/material.dart';", "import 'package:flutter/material.dart';\nimport 'package:flutter/services.dart';")
    open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)

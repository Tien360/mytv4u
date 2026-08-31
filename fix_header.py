import os
content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

import_lines = '''import 'package:flutter/material.dart';
import 'audio_visualizer.dart';
import 'package:id3/id3.dart';
import 'dart:convert';
import 'dart:io';
'''

content = content.replace("import 'package:flutter/material.dart';\\nimport 'audio_visualizer.dart';\\nimport 'package:id3/id3.dart';\\nimport 'dart:convert';\\nimport 'dart:io';\\n", import_lines)
open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)

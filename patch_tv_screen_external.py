import re

with open('lib/screens/tv_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove TvWebViewScreen import
content = content.replace("import 'tv_webview_screen.dart';", "")

# Add missing imports if needed
if "import 'dart:io';" not in content:
    content = content.replace("import 'package:flutter/material.dart';", "import 'dart:io';\nimport 'package:flutter/material.dart';\nimport 'package:window_manager/window_manager.dart';")

# Find and replace _playTvChannel
old_play = '''  void _playTvChannel(TvChannel channel) {
    if (channel.streamUrl.isEmpty && channel.webUrl.isNotEmpty) {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) =>
              TvWebViewScreen(title: channel.name, webUrl: channel.webUrl),
        ),
      );
      return;
    }'''

new_play = '''  void _playTvChannel(TvChannel channel) async {
    if (channel.streamUrl.isEmpty && channel.webUrl.isNotEmpty) {
      if (Platform.isWindows) {
        try {
          final bounds = await windowManager.getBounds();
          final exeDir = File(Platform.resolvedExecutable).parent.path;
          var exePath = '\\\\\tv_web_player.exe';
          if (!File(exePath).existsSync()) {
            exePath = r"T:\\Project\\Phim\\tv_web_player\\bin\\Release\\net8.0-windows\\tv_web_player.exe";
          }
          
          final title = "TV Live - \";
          
          List<String> args = [
            channel.webUrl,
            title,
            bounds.left.toInt().toString(),
            bounds.top.toInt().toString(),
            bounds.width.toInt().toString(),
            bounds.height.toInt().toString(),
          ];
          
          Process.start(exePath, args);
        } catch (e) {
          debugPrint('Error launching external player: \');
        }
      }
      return;
    }'''

content = content.replace(old_play, new_play)

with open('lib/screens/tv_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched tv_screen.dart to use tv_web_player.exe successfully!")

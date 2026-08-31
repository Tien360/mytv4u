import 'dart:io';

void main() {
  var file = File('lib/screens/player_screen.dart');
  var content = file.readAsStringSync();
  content = content.replaceAll(
    'exePath = r"T:\\Project\\Phim\tv_web_player\bin\\Release\net8.0-windows\tv_web_player.exe";',
    'exePath = "T:\\\\Project\\\\Phim\\\\tv_web_player\\\\bin\\\\Release\\\\net8.0-windows\\\\tv_web_player.exe";'
  );
  // Also fix the weird ones with tabs and newlines if they are there
  // Actually, I'll just regex replace the whole if statement
  var pattern = RegExp(r'if \(!File\(exePath\)\.existsSync\(\)\) \{[\s\S]*?\}');
  content = content.replaceFirst(pattern, '''if (!File(exePath).existsSync()) {
        exePath = "T:\\\\Project\\\\Phim\\\\tv_web_player\\\\bin\\\\Release\\\\net8.0-windows\\\\tv_web_player.exe";
      }''');
  file.writeAsStringSync(content);
}

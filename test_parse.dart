import 'dart:io';
import 'dart:convert';

void main() async {
  final res = await Process.run('build\\windows\\x64\\runner\\Release\\yt-dlp.exe', ['-J', 'https://www.youtube.com/watch?v=ZA8V0sVuzJE']);
  print('Exit code: ${res.exitCode}');
  try {
    final json = jsonDecode(res.stdout);
    print('JSON parsed successfully!');
    print('Title: ${json['title']}');
  } catch(e) {
    print('Parse error: $e');
  }
}

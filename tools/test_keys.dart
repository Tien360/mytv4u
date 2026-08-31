import 'dart:io';
import 'dart:convert';
void main() async {
  final ytDlp = File('build/windows/x64/runner/Release/yt-dlp.exe');
  final res = await Process.run(ytDlp.path, ['--dump-json', '--flat-playlist', 'https://www.youtube.com/playlist?list=PLnsrTI5B-0YOE_451Aq8VMMjY_q4b7iQa']);
  if (res.exitCode == 0) {
    final line = res.stdout.toString().split('\n').first;
    final json = jsonDecode(line);
    print(json.keys.toList());
    print('playlist_title: ${json['playlist_title']}');
  }
}

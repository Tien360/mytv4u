import 'dart:io';
import 'dart:convert';

void main() async {
  final url = 'https://www.youtube.com/playlist?list=PLnsrTI5B-0YOE_451Aq8VMMjY_q4b7iQa';
  final ytDlp = File('build/windows/x64/runner/Release/yt-dlp.exe');
  
  print('Running yt-dlp...');
  final res = await Process.run(ytDlp.path, ['--dump-json', '--flat-playlist', url]);
  
  if (res.exitCode == 0) {
    final lines = res.stdout.toString().split('\n').where((l) => l.trim().isNotEmpty).toList();
    print('Found ${lines.length} items');
    for (var i = 0; i < (lines.length > 3 ? 3 : lines.length); i++) {
       final json = jsonDecode(lines[i]);
       print('${json['title']} - ${json['id']} - ${json['url']}');
    }
  } else {
    print('Error: ${res.stderr}');
  }
}

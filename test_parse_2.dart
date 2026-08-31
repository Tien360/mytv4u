import 'dart:io';
import 'dart:convert';

void main() async {
  print('Running yt-dlp...');
  final res = await Process.run('build\\windows\\x64\\runner\\Release\\yt-dlp.exe', ['--no-playlist', '-J', 'https://www.youtube.com/watch?v=ZA8V0sVuzJE&list=RDZA8V0sVuzJE&start_radio=1']);
  print('Exit code: ${res.exitCode}');
  
  try {
    final json = jsonDecode(res.stdout);
    print('JSON parsed successfully!');
    final formats = json['formats'] as List?;
    if (formats != null) {
      final Set<int> heights = {};
      for (var f in formats) {
        if (f['vcodec'] != 'none' && f['height'] != null) {
          heights.add(f['height'] as int);
        }
      }
      print('Heights: $heights');
    } else {
      print('Formats is null');
    }
  } catch(e) {
    print('Parse error: $e');
    print('--- STDOUT START ---');
    print(res.stdout.toString().substring(0, 500)); // print first 500 chars to see what it is
    print('--- STDOUT END ---');
  }
}

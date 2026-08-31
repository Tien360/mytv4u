import 'dart:io';

void main() async {
  print('Testing yt-dlp format extraction...');
  final ytDlp = File('build/windows/x64/runner/Release/yt-dlp.exe');
  final res = await Process.run(ytDlp.path, ['-J', 'https://www.youtube.com/watch?v=jrLexsVpfIw']);
  
  if (res.exitCode == 0) {
    print('Got JSON');
  } else {
    print('Error: ${res.stderr}');
  }
}

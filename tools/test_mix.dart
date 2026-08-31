import 'dart:io';

void main() async {
  final ytDlp = File('build/windows/x64/runner/Release/yt-dlp.exe');
  final res = await Process.run(ytDlp.path, ['--dump-json', '--flat-playlist', 'https://www.youtube.com/watch?v=l0-oRgmei1g&list=RDl0-oRgmei1g&start_radio=1']);
  
  if (res.exitCode == 0) {
    print('Lines: ${res.stdout.toString().split('\n').length}');
  } else {
    print('Error: ${res.stderr}');
  }
}

import 'dart:io';
import 'dart:convert';
import 'package:path/path.dart' as p;

void main() async {
  final localAppData = Platform.environment['LOCALAPPDATA'];
  final defaultWebviewPath = '\\\\\flutter_webview_windows\\\\MyTV4U\\\\EBWebView';
  
  List<String> args = [
    '--cookies-from-browser',
    'edge:\',
    '--dump-json',
    '--flat-playlist',
    '--playlist-end', '5',
    'https://www.youtube.com/watch?v=0cB5SdPbwtc&list=RD0cB5SdPbwtc'
  ];
  
  print('Running yt-dlp with args: \');
  final res = await Process.run('build\\\\windows\\\\x64\\\\runner\\\\Release\\\\yt-dlp.exe', args);
  print('Exit code: \');
  
  if (res.stdout.toString().isNotEmpty) {
    final lines = res.stdout.toString().split('\\n').where((l) => l.trim().isNotEmpty).toList();
    for (var line in lines) {
      try {
        final json = jsonDecode(line);
        print(json['title']);
      } catch(e) {}
    }
  } else {
    print('Error: \');
  }
}

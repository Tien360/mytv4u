import 'dart:io';

void main() async {
  final ebPath = Platform.environment['LOCALAPPDATA']! + '\\\\flutter_webview_windows\\\\MyTV4U\\\\EBWebView';
  print('ebPath: \');
  
  List<String> args = [
    '--cookies-from-browser',
    'edge:\',
    '--dump-json',
    '--flat-playlist',
    '--playlist-end', '5',
    'https://www.youtube.com/watch?v=0cB5SdPbwtc&list=RD0cB5SdPbwtc'
  ];
  
  final res = await Process.run('build\\\\windows\\\\x64\\\\runner\\\\Release\\\\yt-dlp.exe', args);
  print('Exit code: \');
  print('Stdout empty? \');
  print('Stderr: \');
}

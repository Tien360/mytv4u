import 'dart:io';
import 'dart:convert';

void main() async {
  final ytDlp = File('build/windows/x64/runner/Release/yt-dlp.exe');
  final res = await Process.run(ytDlp.path, ['-J', 'https://www.youtube.com/watch?v=jrLexsVpfIw']);
  
  if (res.exitCode == 0) {
    final json = jsonDecode(res.stdout);
    final formats = json['formats'] as List;
    final Set<int> heights = {};
    for (var f in formats) {
      if (f['vcodec'] != 'none' && f['height'] != null) {
        heights.add(f['height'] as int);
      }
    }
    final sortedHeights = heights.toList()..sort();
    print('Available heights: $sortedHeights');
  }
}

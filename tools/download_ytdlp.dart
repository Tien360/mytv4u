import 'dart:io';
import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  print('Downloading yt-dlp.exe...');
  final url = 'https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe';
  
  final destRelease = File('build/windows/x64/runner/Release/yt-dlp.exe');
  
  try {
    if (!destRelease.parent.existsSync()) {
      destRelease.parent.createSync(recursive: true);
    }
    
    if (destRelease.existsSync()) {
      print('yt-dlp.exe already exists, checking size...');
      if (destRelease.lengthSync() > 10000000) { // roughly 10MB
        print('yt-dlp.exe is already present and seems valid. Done.');
        return;
      }
    }

    final response = await http.get(Uri.parse(url));
    if (response.statusCode == 200 || response.statusCode == 302) {
      destRelease.writeAsBytesSync(response.bodyBytes);
      print('Downloaded successfully to: ${destRelease.path}');
    } else {
      print('Failed to download: HTTP ${response.statusCode}');
    }
  } catch (e) {
    print('Error downloading yt-dlp: $e');
  }
}

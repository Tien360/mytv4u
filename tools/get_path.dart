import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;
import 'dart:io';

void main() async {
  final appDataDir = await getApplicationSupportDirectory();
  final profileDir = p.join(appDataDir.path, 'youtube_webview_profile');
  print(profileDir);
}

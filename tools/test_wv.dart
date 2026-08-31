import 'package:webview_windows/webview_windows.dart';
import 'dart:io';
import 'package:path/path.dart' as p;

void main() async {
  final controller = WebviewController();
  final dataDir = p.join(Directory.current.path, 'webview_test_profile');
  await controller.initialize(userDataFolder: dataDir);
  await controller.loadUrl('https://www.youtube.com');
  print('WebView initialized at $dataDir');
  // Just exit after 5 seconds
  await Future.delayed(Duration(seconds: 5));
  exit(0);
}

import 'package:webview_windows/webview_windows.dart';
import 'dart:io';
import 'package:path/path.dart' as p;

void main() async {
  try {
    await WebviewController.initializeEnvironment(userDataPath: p.join(Directory.current.path, 'wv2_test'));
    final controller = WebviewController();
    await controller.initialize();
    await controller.loadUrl('https://www.youtube.com');
    await Future.delayed(Duration(seconds: 4));
    exit(0);
  } catch (e) {}
}

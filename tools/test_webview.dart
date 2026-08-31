import 'package:webview_windows/webview_windows.dart';
void main() {
  final c = WebviewController();
  // We just want to check if the method exists in analysis
  print(c.getCookies);
}

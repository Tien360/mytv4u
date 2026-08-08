import 'package:webview_windows/webview_windows.dart';

void main() async {
  final controller = WebviewController();
  await controller.setPopupWindowPolicy(WebviewPopupWindowPolicy.deny);
  print('Success');
}

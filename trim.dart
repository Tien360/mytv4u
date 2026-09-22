import 'dart:io';

void main() {
  var file = File('lib/screens/yt_player_screen.dart');
  var content = file.readAsStringSync();
  
  // Clean up unused imports
  content = content.replaceAll(RegExp(r\"import '../api/premium_resolver.dart';\\n\"), '');
  content = content.replaceAll(RegExp(r\"import '../api/opensubtitles_api.dart';\\n\"), '');
  content = content.replaceAll(RegExp(r\"import '../api/skip_segments_api.dart';\\n\"), '');
  content = content.replaceAll(RegExp(r\"import 'package:webview_windows/webview_windows.dart';\\n\"), '');
  
  // Let's remove the _buildMotchillServerList and _buildEmbedServerList functions
  content = content.replaceAll(RegExp(r\"Widget _buildMotchillServerList\\(\\)[\\s\\S]*?Widget _buildEmbedServerList\\(\\)[\\s\\S]*?Widget _buildQualityServerList\\(\\)\"), 'Widget _buildQualityServerList()');
  
  // It's safer to not blindly remove everything by regex because it might break curly braces.
  
  file.writeAsStringSync(content);
}

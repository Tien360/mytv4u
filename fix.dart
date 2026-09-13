import 'dart:io';

void main() {
  final file = File('lib/screens/movie_detail_screen.dart');
  String text = file.readAsStringSync();
  
  text = text.replaceAll(
    "cleanMovieName = cleanMovieName.replaceAll(RegExp(r'(?i)(\\s*-\\s*)?(ph?n|season|part)\\s*\\d+'), '').trim();",
    "cleanMovieName = cleanMovieName.replaceAll(RegExp(r'(\\s*-\\s*)?(phần|season|part)\\s*\\d+', caseSensitive: false), '').trim();"
  );
  
  text = text.replaceAll(
    "cleanServerName = cleanServerName.replaceAll(RegExp(r'(?i)premium\\s*-\\s*'), '').trim();",
    "cleanServerName = cleanServerName.replaceAll(RegExp(r'premium\\s*-\\s*', caseSensitive: false), '').trim();"
  );

  file.writeAsStringSync(text);
  print("Fixed RegExp in movie_detail_screen.dart");
}

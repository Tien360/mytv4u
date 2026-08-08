import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  String cleanTitle(String title) {
    // Regex to match "Season X", "Phần X", "Part X" at the end of string or anywhere
    final regex = RegExp(r'(?:\s*-\s*)?(?:season|phần|part)\s*\d+', caseSensitive: false);
    return title.replaceAll(regex, '').trim();
  }

  print(cleanTitle('Lupin Phần 3'));
  print(cleanTitle('The Boys Season 3'));
  print(cleanTitle('Money Heist - Part 5'));
  print(cleanTitle('Sex Education Season 4'));
  print(cleanTitle('Thư Ký Kim Sao Thế'));
}

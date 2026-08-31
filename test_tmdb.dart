import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final apiKey = 'e9e9d8da18ae29fc430845952232787c';
  final url = 'https://api.themoviedb.org/3/tv/312573/season/1?api_key=$apiKey&language=vi-VN';
  final res = await http.get(Uri.parse(url));
  print(res.statusCode);
  try {
    final data = json.decode(utf8.decode(res.bodyBytes));
    print('Decode success, length: ${data['episodes'].length}');
  } catch (e) {
    print('DECODE ERROR: $e');
  }
}

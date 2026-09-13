import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final imdbId = 'tt14688458';
  final season = 1;
  final episode = 4;

  final endpoints = [
    'https://api.theintrodb.org/v3/media?imdb_id=$imdbId&season=$season&episode=$episode',
    'https://api.skipdb.tv/api/segments?imdb_id=$imdbId&season=$season&episode=$episode',
  ];

  for (String url in endpoints) {
    try {
      final res = await http.get(
        Uri.parse(url),
        headers: {
          'User-Agent': 'Mozilla/5.0',
          'X-API-Key': 'a9fb57dba1eea9bc3e660a909d838d726e3bf623d52620282013481d1f6e5377',
        }
      );
      print('$url -> ${res.statusCode}');
      if (res.statusCode == 200) {
        print(res.body);
      }
    } catch (_) {}
  }
}

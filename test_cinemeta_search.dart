import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final query = Uri.encodeComponent('avatar');
  final url = 'https://v3-cinemeta.strem.io/catalog/movie/top/search=$query.json';
  print('Fetching: $url');
  final res = await http.get(Uri.parse(url));
  if (res.statusCode == 200) {
      final data = json.decode(res.body);
      final metas = data['metas'] as List<dynamic>?;
      if (metas != null && metas.isNotEmpty) {
          for (var meta in metas.take(3)) {
              print('---');
              print('Name: ${meta['name']}');
              print('Type: ${meta['type']}');
              print('IMDB: ${meta['imdb_id']}');
              print('Poster: ${meta['poster']}');
          }
      } else {
          print('No results found.');
      }
  } else {
      print('HTTP ${res.statusCode}');
  }
}

import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final url = 'https://v3-cinemeta.strem.io/catalog/movie/top.json';
  print('Fetching: $url');
  final res = await http.get(Uri.parse(url));
  if (res.statusCode == 200) {
      final data = json.decode(res.body);
      final metas = data['metas'] as List<dynamic>?;
      if (metas != null && metas.isNotEmpty) {
          print('Total top movies: ${metas.length}');
          for (var meta in metas.take(3)) {
              print('---');
              print('Name: ${meta['name']}');
              print('Type: ${meta['type']}');
              print('IMDB: ${meta['imdb_id']}');
          }
      }
  }
}

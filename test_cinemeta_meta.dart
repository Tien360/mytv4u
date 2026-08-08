import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final imdbId = 'tt0111161'; // The Shawshank Redemption
  final url = 'https://v3-cinemeta.strem.io/meta/movie/$imdbId.json';
  print('Fetching: $url');
  final res = await http.get(Uri.parse(url));
  if (res.statusCode == 200) {
      final data = json.decode(res.body);
      final meta = data['meta'] as Map<String, dynamic>?;
      if (meta != null) {
          print('Name: ${meta['name']}');
          print('Poster: ${meta['poster']}');
          print('Background: ${meta['background']}');
          print('Description: ${meta['description']}');
          print('Year: ${meta['year']}');
          print('Runtime: ${meta['runtime']}');
          print('Director: ${meta['director']}');
          print('Cast: ${meta['cast']}');
          print('Genres: ${meta['genre']}');
      }
  }
}

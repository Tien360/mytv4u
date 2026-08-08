import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  print('--- SERIES ---');
  final url1 = 'https://torrentio.strem.fun/stream/series/tt8242904:1:1.json';
  final res1 = await http.get(Uri.parse(url1));
  if (res1.statusCode == 200) {
    final data = json.decode(res1.body);
    final streams = data['streams'] as List?;
    if (streams != null) {
      for (int i = 0; i < 5 && i < streams.length; i++) {
        print(streams[i]['title']);
      }
    }
  }

  print('\n--- MOVIE ---');
  final url2 = 'https://torrentio.strem.fun/stream/movie/tt8242904.json';
  final res2 = await http.get(Uri.parse(url2));
  if (res2.statusCode == 200) {
    final data = json.decode(res2.body);
    final streams = data['streams'] as List?;
    if (streams != null) {
      for (int i = 0; i < 5 && i < streams.length; i++) {
        print(streams[i]['title']);
      }
    }
  }
}

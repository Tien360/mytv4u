import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final url = 'https://v3-cinemeta.strem.io/meta/series/tt8242904.json';
  final res = await http.get(Uri.parse(url));
  final data = json.decode(res.body);
  print(data['meta']?['name']);
  final videos = data['meta']?['videos'] as List?;
  print('Episodes: ${videos?.length}');
  if (videos != null && videos.isNotEmpty) {
    print(videos[0]);
  }
}

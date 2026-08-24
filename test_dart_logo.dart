import 'package:http/http.dart' as http;
import 'dart:convert';

void main() async {
  String tmdbApiKey = 'e9e9d8da18ae29fc430845952232787c';
  final searchUrl = 'https://api.themoviedb.org/3/search/multi?query=Pull%20Strings&api_key=$tmdbApiKey&language=en-US';
  final res = await http.get(Uri.parse(searchUrl));
  final data = json.decode(res.body);
  final match = data['results'][0];
  print('Type: ${match['media_type']}, ID: ${match['id']}');

  final imgUrl = 'https://api.themoviedb.org/3/${match['media_type']}/${match['id']}/images?api_key=$tmdbApiKey';
  final imgRes = await http.get(Uri.parse(imgUrl));
  final imgData = json.decode(imgRes.body);
  final logos = imgData['logos'] as List;

  List<String?> priorities = ['vi', 'en', 'xx', null, ''];
  for (String? lang in priorities) {
    var targetLogo = logos.firstWhere(
      (l) => l['iso_639_1'] == lang,
      orElse: () => null,
    );
    if (targetLogo != null) {
      print('Selected Logo Lang: ${targetLogo['iso_639_1'] ?? 'none'}');
      return;
    }
  }
  print('Selected Logo Lang: none');
}

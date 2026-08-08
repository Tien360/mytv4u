import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final tmdbApiKey = 'e9e9d8da18ae29fc430845952232787c';
  final query = Uri.encodeComponent("What's Wrong with Secretary Kim");
  final searchUrl = 'https://api.themoviedb.org/3/search/tv?query=$query&api_key=$tmdbApiKey&language=en-US';
  print('Search: $searchUrl');
  final res = await http.get(Uri.parse(searchUrl));
  final data = json.decode(res.body);
  print(data['results'][0]);
  
  final tmdbId = data['results'][0]['id'];
  final extUrl = 'https://api.themoviedb.org/3/tv/$tmdbId/external_ids?api_key=$tmdbApiKey';
  final extRes = await http.get(Uri.parse(extUrl));
  final extData = json.decode(extRes.body);
  print('IMDB ID: ${extData['imdb_id']}');
}

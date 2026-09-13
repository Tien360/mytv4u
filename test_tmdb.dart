import 'package:http/http.dart' as http;
import 'dart:convert';
void main() async {
  final query = Uri.encodeComponent('Silo ( )');
  final searchUrl = 'https://api.themoviedb.org/3/search/tv?query=$query&api_key=e9e9d8da18ae29fc430845952232787c&language=en-US';
  final res = await http.get(Uri.parse(searchUrl));
  print(res.body);
}

import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final apiKey = 'e9e9d8da18ae29fc430845952232787c';
  final url = 'https://api.themoviedb.org/3/movie/936054?api_key=$apiKey&append_to_response=credits'; // Example movie
  final res = await http.get(Uri.parse(url));
  print(res.statusCode);
}

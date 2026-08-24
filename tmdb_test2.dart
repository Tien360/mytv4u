import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final apiKey = 'e9e9d8da18ae29fc430845952232787c';
  // Minions: The Rise of Gru (Minions 2) id is 438148. Minions is 211672
  final url = 'https://api.themoviedb.org/3/movie/438148?api_key=$apiKey'; 
  final res = await http.get(Uri.parse(url));
  final data = json.decode(res.body);
  print('Budget: ${data['budget']} (${data['budget'].runtimeType})');
  print('Revenue: ${data['revenue']} (${data['revenue'].runtimeType})');
}

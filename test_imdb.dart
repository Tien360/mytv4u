import 'package:http/http.dart' as http;
import 'dart:convert';
void main() async {
  final url = 'https://tv-v2.api-fetch.website/shows/1?sort=rating&order=-1&genre=all&keywords=Silo';
  try {
      final res = await http.get(Uri.parse(url));
      print(res.body);
  } catch(e) { print(e); }
}

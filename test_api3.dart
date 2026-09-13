import 'dart:convert';
import 'package:http/http.dart' as http;
void main() async {
  final url = 'https://api.theintrodb.org/v3/media?imdb_id=tt14688458&season=1&episode=3';
  final res = await http.get(Uri.parse(url), headers: {'User-Agent': 'Mozilla/5.0', 'X-API-Key': 'a9fb57dba1eea9bc3e660a909d838d726e3bf623d52620282013481d1f6e5377'});
  print(res.statusCode);
  print(res.body);
}

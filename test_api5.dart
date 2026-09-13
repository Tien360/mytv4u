import 'dart:convert';
import 'package:http/http.dart' as http;
void main() async {
  final url = 'https://api.introdb.app/segments?imdb_id=tt14688458&season=1&episode=3';
  final res = await http.get(Uri.parse(url), headers: {'User-Agent': 'Mozilla/5.0'});
  print("introdb.app status: " + res.statusCode.toString());
  if (res.statusCode == 200) {
    print(res.body);
  }
}

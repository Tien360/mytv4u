import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final res = await http.get(Uri.parse('https://phimapi.com/phim/cuu-long-thanh-trai-vay-thanh'));
  final data = json.decode(res.body);
  print(data['movie']['episode_current']);
  print(data['movie']['episode_total']);
}

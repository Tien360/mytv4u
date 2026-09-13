import 'package:http/http.dart' as http;
import 'dart:convert';
void main() async {
  final res = await http.get(Uri.parse('https://phimapi.com/phim/ham-silo-phan-2'));
  final data = json.decode(res.body);
  print(data['movie']['name']);
  print(data['movie']['origin_name']);
}

import 'package:http/http.dart' as http;
import 'dart:convert';
void main() async {
  final res = await http.get(Uri.parse('https://dogtail.oxaliplatin.workers.dev/api/premium/movies?keyword=Silo'));
  print(res.body);
}

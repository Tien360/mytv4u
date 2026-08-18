import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final url = 'https://dogtail.oxaliplatin.workers.dev/api/premium/detail/khi-anh-chay-ve-phia-em';
  final res = await http.get(Uri.parse(url));
  print(res.body);
}

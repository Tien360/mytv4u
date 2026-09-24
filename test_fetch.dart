import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final url = 'https://medata.phim4k.workers.dev/?id=2TNH8E1NYMZQI1B9';
  try {
    final res = await http.get(Uri.parse(url), headers: {'User-Agent': 'Mozilla/5.0'});
    print(res.body);
  } catch (e) {
    print(e);
  }
}

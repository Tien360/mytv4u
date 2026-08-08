import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final res = await http.get(Uri.parse('https://dogtail.oxaliplatin.workers.dev/api/premium/detail/phien-toa-dinh-menh'));
  if (res.statusCode == 200) {
    final data = json.decode(res.body);
    final movie = data['movie'];
    print('Trailer URL: ${movie['trailer_url']}');
  } else {
    print('Failed: ${res.statusCode}');
  }
}

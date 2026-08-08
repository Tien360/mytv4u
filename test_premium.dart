import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final res = await http.get(Uri.parse('https://dogtail.oxaliplatin.workers.dev/api/premium/movies?page=1'));
  if (res.statusCode == 200) {
    final data = json.decode(res.body);
    final items = data['items'] as List;
    if (items.isNotEmpty) {
      final slug = items[0]['slug'];
      print('Found slug: $slug');
      final detailRes = await http.get(Uri.parse('https://dogtail.oxaliplatin.workers.dev/api/premium/detail/$slug'));
      if (detailRes.statusCode == 200) {
         final detailData = json.decode(detailRes.body);
         print('Casts: ${detailData['movie']['casts']}');
         print('Directors: ${detailData['movie']['directors']}');
      }
    }
  } else {
    print('Failed: ${res.statusCode}');
  }
}

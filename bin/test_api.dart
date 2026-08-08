import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  try {
    final url = 'https://dogtail.oxaliplatin.workers.dev/api/premium/movies?page=1';
    final res = await http.get(Uri.parse(url)).timeout(const Duration(seconds: 5));
    print('Hero: ${res.statusCode}');
    if (res.statusCode == 200) {
      final data = json.decode(res.body);
      final items = (data['items'] as List?) ?? [];
      print('Hero Items: ${items.length}');
    }

    final url2 = 'https://dogtail.oxaliplatin.workers.dev/api/premium/movies?page=1&filterType=danh-sach&filterValue=phim-le';
    final res2 = await http.get(Uri.parse(url2)).timeout(const Duration(seconds: 5));
    print('Category: ${res2.statusCode}');
    if (res2.statusCode == 200) {
      final data = json.decode(res2.body);
      final items = (data['items'] as List?) ?? [];
      print('Category Items: ${items.length}');
    }
  } catch (e) {
    print('Exception: $e');
  }
}

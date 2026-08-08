import 'dart:convert';
import 'package:http/http.dart' as http;
import '../lib/models/movie.dart';

void main() async {
  try {
    final url = 'https://dogtail.oxaliplatin.workers.dev/api/premium/movies?page=1&filterType=danh-sach&filterValue=phim-le';
    final res = await http.get(Uri.parse(url)).timeout(const Duration(seconds: 5));
    if (res.statusCode == 200) {
      final data = json.decode(res.body);
      final items = (data['items'] as List?) ?? [];
      for (var e in items) {
        try {
          var m = Movie.fromJson(e as Map<String, dynamic>, defaultSource: 'premium');
          print('Parsed: ${m.name}');
        } catch (e) {
          print('Error parsing: $e');
        }
      }
    }
  } catch (e) {
    print('Exception: $e');
  }
}

import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final Map<String, String> endpoints = {
    'NguonC': 'https://phim.nguonc.com/api/films/phim-moi-cap-nhat?page=1',
    'KKPhim': 'https://phimapi.com/danh-sach/phim-moi-cap-nhat?page=1',
    'Ophim': 'https://ophim1.com/danh-sach/phim-moi-cap-nhat?page=1',
    'VSMov': 'https://vsmov.com/api/danh-sach?type=phim-moi-cap-nhat&page=1',
    'Phim4K': 'https://phim4k.top/api/films/phim-moi-cap-nhat?page=1',
    'Premium': 'https://dogtail.oxaliplatin.workers.dev/api/premium',
  };

  for (var entry in endpoints.entries) {
    print('--- ${entry.key} ---');
    try {
      final res = await http.get(Uri.parse(entry.value));
      final data = json.decode(res.body);
      
      List items = [];
      if (data['items'] != null) items = data['items'];
      else if (data['data'] != null && data['data']['items'] != null) items = data['data']['items'];
      else if (data['data'] != null && data['data']['movies'] != null) items = data['data']['movies']; // For Premium? Wait, let's check what premium returns
      else if (data is List) items = data;

      if (items.isNotEmpty) {
        final item = items.first;
        final keys = item.keys.where((k) => k.contains('time') || k.contains('date') || k.contains('modified') || k.contains('updated')).toList();
        print('Available time-related keys: $keys');
        for (var k in keys) {
          print('  $k: ${item[k]}');
        }
        if (keys.isEmpty) {
             print('  No time-related keys found in first item. Full item keys: ${item.keys}');
        }
      } else {
        print('  No items found in response.');
      }
    } catch (e) {
      print('  Error: $e');
    }
  }
}

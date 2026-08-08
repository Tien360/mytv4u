import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final slug = '23-000-sinh-mang';
  
  // Test KKPhim
  final url1 = 'https://phimapi.com/v1/api/phim/$slug';
  final res1 = await http.get(Uri.parse(url1));
  final data1 = json.decode(res1.body);
  print('KKPhim keys: ${data1.keys}');
  if (data1['data'] != null) {
    print('KKPhim data keys: ${data1['data'].keys}');
    if (data1['data']['item'] != null) {
      print('KKPhim item keys: ${data1['data']['item'].keys}');
      final eps = data1['data']['item']['episodes'];
      print('KKPhim episodes isList: ${eps is List}, length: ${eps?.length}');
    }
  }
  
  // Test Ophim
  final url2 = 'https://ophim1.com/phim/$slug';
  final res2 = await http.get(Uri.parse(url2));
  final data2 = json.decode(res2.body);
  print('Ophim keys: ${data2.keys}');
  print('Ophim episode isList: ${data2['episodes'] is List}, length: ${data2['episodes']?.length}');
  print('Ophim episode (no s) isList: ${data2['episode'] is List}, length: ${data2['episode']?.length}');
}

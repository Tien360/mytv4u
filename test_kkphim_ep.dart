import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final slug = '23-000-sinh-mang';
  
  // Test KKPhim
  final url1 = 'https://phimapi.com/v1/api/phim/$slug';
  final res1 = await http.get(Uri.parse(url1));
  final data1 = json.decode(res1.body);
  
  if (data1['data'] != null && data1['data']['item'] != null) {
    final eps = data1['data']['item']['episodes'];
    if (eps != null && eps.isNotEmpty) {
      final firstServer = eps[0];
      print('First server keys: ${firstServer.keys}');
      final serverData = firstServer['server_data'];
      if (serverData != null && serverData.isNotEmpty) {
        final firstEp = serverData[0];
        print('First episode keys: ${firstEp.keys}');
        print('First episode data: $firstEp');
      }
    }
  }
}

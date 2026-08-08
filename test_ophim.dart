import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  try {
    final res = await http.get(Uri.parse('https://ophim1.com/v1/api/phim/cho-hoang-va-xuong')).timeout(Duration(seconds: 5));
    print('Status: ${res.statusCode}');
    if (res.statusCode == 200) {
      final data = json.decode(res.body);
      print('Status from JSON: ${data['status']}');
      final eps = (data['movie'] != null) ? data['movie']['episodes'] : (data['item'] != null ? data['item']['episodes'] : null);
      if (eps != null) {
        for (var s in eps) {
          print('Server: ${s['server_name']}');
        }
      } else {
        print('No episodes array found');
      }
    }
  } catch (e) {
    print('Error: $e');
  }
}

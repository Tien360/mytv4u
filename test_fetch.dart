import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  String id = '8M6NIBQJ5VQP';
  
  try {
    final url = 'https://medata.phim4k.workers.dev/?id=$id';
    print('Fetching: $url');
    final res = await http.get(
      Uri.parse(url),
      headers: {'User-Agent': 'Mozilla/5.0'}
    ).timeout(const Duration(seconds: 4));
    
    print('Response: ${res.statusCode}');
    if (res.statusCode == 200) {
      final data = json.decode(res.body);
      final resStr = (data['resolution'] ?? '').toString().toUpperCase();
      print('resStr: $resStr');
      int score = 1;
      if (resStr.contains('4K') || resStr.contains('2160')) score = 4;
      else if (resStr.contains('1080')) score = 3;
      else if (resStr.contains('720')) score = 2;
      
      print('Score: $score');
    }
  } catch (e) {
    print('Error: $e');
  }
}

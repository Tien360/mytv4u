import 'dart:convert';
import 'package:http/http.dart' as http;

class ConfigApi {
  // Thay đổi URL này nếu bạn đổi tên repo hoặc branch
  static const String _configUrl = 'https://raw.githubusercontent.com/Tien360/mytv4u/master/streaming_config.json';

  static Future<List<String>> getFallbackDomains() async {
    try {
      // Thêm cache-bust để tránh GitHub cache file json quá lâu (tùy chọn)
      final url = Uri.parse('$_configUrl?t=${DateTime.now().millisecondsSinceEpoch}');
      final response = await http.get(url).timeout(const Duration(seconds: 10));
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['premiumDomains'] != null) {
          final array = data['premiumDomains'] as List<dynamic>;
          if (array.isNotEmpty) {
            return array.map((e) => e.toString()).toList();
          }
        }
      }
    } catch (e) {
      print('Error fetching fallback domains from GitHub: $e');
    }
    
    // Fallback mặc định nếu GitHub lỗi
    return [
      'sv1.p4k.dpdns.org',
      'sv2.p4k.dpdns.org',
    ];
  }
}

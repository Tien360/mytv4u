import 'dart:convert';
import 'package:http/http.dart' as http;

class TranslateApi {
  static Future<String?> translateEnToVi(String text) async {
    if (text.isEmpty) return null;
    try {
      final url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=vi&dt=t&q=${Uri.encodeComponent(text)}';
      final res = await http.get(Uri.parse(url)).timeout(const Duration(seconds: 5));
      if (res.statusCode == 200) {
        final data = json.decode(utf8.decode(res.bodyBytes));
        final sentences = data[0] as List;
        String translated = '';
        for (var s in sentences) {
          translated += s[0];
        }
        return translated;
      }
    } catch (e) {
      print('Lỗi dịch Google Translate: $e');
    }
    return null;
  }
}

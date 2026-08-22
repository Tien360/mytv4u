import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  String version = '26.08.20.b.beta';
  String notes = '''🚀 Cập nhật Phiên bản 26.08.20.b.beta

🛠️ Cải tiến & Sửa lỗi:
- Khắc phục: Dịch lại toàn bộ các nhãn bị thiếu (như bàn phím, player_screen, tv_screen) sang Tiếng Việt và Tiếng Anh.''';

  final url = Uri.parse('https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/beta');
  final body = {
    "fields": {
      "latest_version": {"stringValue": version},
      "download_url": {"stringValue": "https://github.com/Tien360/mytv4u/releases/download/$version/MyTV4U_Setup_$version.exe"},
      "release_notes": {"stringValue": notes},
      "is_force_update": {"booleanValue": false}
    }
  };
  
  final res = await http.patch(
    url, 
    headers: {'Content-Type': 'application/json; charset=UTF-8'},
    body: json.encode(body)
  );
  print(res.statusCode);
  print(res.body);
}

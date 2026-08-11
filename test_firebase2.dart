import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

void main() async {
  final url = Uri.parse('https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/beta');
  
  final body = {
    "fields": {
      "latest_version": {"stringValue": "26.08.11.a.beta"},
      "download_url": {"stringValue": "https://github.com/Tien360/mytv4u/releases/download/26.08.11.a.beta/MyTV4U_Setup_26.08.11.a.beta.exe"},
      "release_notes": {"stringValue": "- Phân bổ RAM động cho Stremio Server giúp khai thác sức mạnh phần cứng.\n- Tối ưu bộ đệm hình ảnh (Image Cache) giúp app nhẹ hơn, giảm tải CPU."},
      "is_force_update": {"booleanValue": false}
    }
  };

  final res = await http.patch(url, body: json.encode(body));
  print(res.statusCode);
  print(res.body);
}
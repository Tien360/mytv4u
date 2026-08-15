import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

void main() async {
  final url = Uri.parse('https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/beta');
  
  final body = {
    "fields": {
      "latest_version": {"stringValue": "26.08.15.a.beta"},
      "download_url": {"stringValue": "https://github.com/Tien360/mytv4u/releases/download/26.08.15.a.beta/MyTV4U_Setup_26.08.15.a.beta.exe"},
      "release_notes": {"stringValue": "- Ra mắt chức năng Thể Thao (Bóng Đá) trực tiếp.\n- Hỗ trợ đổi luồng bình luận viên tự do.\n- Nâng cấp Trình phát Gốc để phát mượt mà m3u8 từ nguồn thể thao."},
      "is_force_update": {"booleanValue": false}
    }
  };

  final res = await http.patch(url, body: json.encode(body));
  print(res.statusCode);
  print(res.body);
}
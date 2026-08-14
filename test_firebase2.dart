import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

void main() async {
  final url = Uri.parse('https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/beta');
  
  final body = {
    "fields": {
      "latest_version": {"stringValue": "26.08.14.m.beta"},
      "download_url": {"stringValue": "https://github.com/Tien360/mytv4u/releases/download/26.08.14.m.beta/MyTV4U_Setup_26.08.14.m.beta.exe"},
      "release_notes": {"stringValue": "- Sửa lỗi rác màn hình và Error Decoding Audio khi xem HBO bằng mpv.\n- Các kênh có chuẩn mã hoá phức tạp (.mpd/DRM) giờ đây đều được fallback an toàn 100% qua WebView siêu mượt."},
      "is_force_update": {"booleanValue": false}
    }
  };

  final res = await http.patch(url, body: json.encode(body));
  print(res.statusCode);
  print(res.body);
}
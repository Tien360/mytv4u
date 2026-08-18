import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  String version = '26.08.18.d.beta';
  String notes = '- Thêm Bộ lọc màu Video (Sống động, Rạp phim, Đen trắng...)\n- Thêm Tinh chỉnh độ trễ Phụ đề & Âm thanh.';
  String channel = 'beta';

  final url = Uri.parse('https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/$channel');
  final body = {
    "fields": {
      "latest_version": {"stringValue": version},
      "release_notes": {"stringValue": notes},
      "download_url": {"stringValue": "https://github.com/Tien360/mytv4u/releases/download/$version/MyTV4U_Setup_$version.exe"},
      "is_force_update": {"booleanValue": false},
      "release_date": {"timestampValue": DateTime.now().toUtc().toIso8601String()}
    }
  };

  final res = await http.patch(
    url, 
    headers: {'Content-Type': 'application/json; charset=UTF-8'},
    body: json.encode(body)
  );

  if (res.statusCode == 200) {
    print('Cập nhật Firebase ($channel) thành công!');
  } else {
    print('Lỗi Firebase: ${res.statusCode} ${res.body}');
  }
}

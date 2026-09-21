import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final version = '26.09.14.30.public';
  final notes = 'Sửa lỗi nhận diện sai Season & Hiển thị chính xác luồng Âm thanh/Phụ đề đang chọn';
  final isForceUpdate = false;
  final channel = 'public';
  
  final url = Uri.parse('https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/$channel');
  final body = {
    'fields': {
      'latest_version': {'stringValue': version},
      'download_url': {'stringValue': 'https://github.com/Tien360/mytv4u/releases/download/$version/MyTV4U_Setup_${version}.exe'},
      'release_notes': {'stringValue': notes},
      'is_force_update': {'booleanValue': isForceUpdate}
    }
  };

  await http.patch(url, headers: {'Content-Type': 'application/json; charset=UTF-8'}, body: json.encode(body));
  await http.patch(Uri.parse('https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/latest'), headers: {'Content-Type': 'application/json; charset=UTF-8'}, body: json.encode(body));
}

import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final version = '26.08.09.d.beta';
  final notes = 'Sửa lỗi tự nhảy tập khi Stremio đang tải bộ đệm';
  final channel = 'beta';
  
  final url = Uri.parse('https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/$channel');
  
  final body = {
    'fields': {
      'latest_version': {'stringValue': version},
      'release_notes': {'stringValue': notes},
      'download_url': {'stringValue': 'https://github.com/Tien360/mytv4u/releases/download/$version/MyTV4U_Setup_$version.exe'},
      'is_force_update': {'booleanValue': false},
      'release_date': {'timestampValue': DateTime.now().toUtc().toIso8601String()},
    }
  };

  print('Đang cập nhật Firebase ($channel)...');
  final res = await http.patch(
    url, 
    headers: {'Content-Type': 'application/json; charset=UTF-8'},
    body: json.encode(body)
  );
  
  if (res.statusCode == 200) {
    print('Thành công!');
  } else {
    print('Lỗi Firebase: ${res.statusCode} ${res.body}');
  }
}

import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';

void main() async {
    String version = '26.08.23.n.beta';
    String notes = '- Hỗ trợ đa ngôn ngữ cho logo phim trên TMDB (ưu tiên hiển thị logo tiếng Việt, dự phòng logo tiếng Anh)\n- Tối ưu hóa việc hiển thị tên phim, tên gốc khi kết hợp cùng logo, tránh lặp chữ\n- Thêm viền mờ cho logo để chống chìm vào nền tối\n- Cập nhật hotfix sửa lỗi mất badge giao diện triệt để';
    
    print('Đang cập nhật đường link lên Firebase...');
    String channel = 'public';
    if (version.contains('.beta')) channel = 'beta';
    if (version.contains('.dev')) channel = 'dev';

    final url = Uri.parse('https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/$channel');
    final body = {
      'fields': {
        'latest_version': {'stringValue': version},
        'download_url': {'stringValue': 'https://github.com/Tien360/mytv4u/releases/download/$version/MyTV4U_Setup_$version.exe'},
        'release_notes': {'stringValue': notes},
        'is_force_update': {'booleanValue': true}
      }
    };
    
    try {
      final response = await http.patch(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      );
      if (response.statusCode == 200 || response.statusCode == 201) {
        print('-> Cập nhật Firebase thành công!');
      } else {
        print('-> LỖI CẬP NHẬT FIREBASE! ${response.body}');
      }
    } catch (e) {
      print('-> LỖI CẬP NHẬT FIREBASE! $e');
    }
}

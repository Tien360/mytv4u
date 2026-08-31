import 'dart:convert';
import 'package:http/http.dart' as http;
import 'dart:io';

void main() async {
  String version = '26.08.25.1.public';
  String notes = '''1. Tối ưu tìm kiếm Trailer TMDB (Hỗ trợ chính xác mọi ngôn ngữ, đặc biệt phim Châu Á).
2. Nâng cấp Trình phát Web: Chuyển kênh TV & Web sang lõi C# mượt mà hơn.
3. Tích hợp AdBlocker chặn quảng cáo & dọn rác giao diện web.
4. Fix triệt để lỗi font tiếng Việt trên toàn hệ thống.
5. Nâng cấp hệ thống OTA cốt lõi (Hỗ trợ Build Promotion siêu tốc).''';

  final url = Uri.parse('https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/public');
  final githubUrl = 'https://github.com/Tien360/mytv4u/releases/download/$version/MyTV4U_Setup_$version.exe';

  final body = json.encode({
    'fields': {
      'latest_version': {'stringValue': version},
      'release_notes': {'stringValue': notes},
      'download_url': {'stringValue': githubUrl},
      'is_mandatory': {'booleanValue': false}
    }
  });

  final response = await http.patch(url, body: body, headers: {'Content-Type': 'application/json'});
  
  if (response.statusCode == 200) {
    print('Thành công đẩy lên Firebase bản $version!');
  } else {
    print('Lỗi Firebase: ${response.statusCode} - ${response.body}');
    exit(1);
  }
}

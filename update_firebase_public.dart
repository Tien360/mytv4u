import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  String version = '26.08.24.v.public';
  String notes = '- Ra mắt Hệ thống Hiệu ứng Tương tác (Easter Egg) siêu mượt với hơn 100 sticker tĩnh, động và 3D\n- Thêm hiệu ứng Jumpscare hù dọa thót tim khi xem phim Kinh Dị\n- Chuyển cài đặt Easter Egg vào mục Sức khỏe & Hệ thống trực quan hơn\n- Màn tri ân Huyền Thoại Nhóm 4 rực rỡ pháo hoa toàn màn hình';
  
  for (String channel in ['public', 'latest']) {
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
      print('Lỗi Firebase ($channel): ${res.statusCode} ${res.body}');
    }
  }
}

import 'dart:convert';
import 'package:http/http.dart' as http;
import 'dart:io';

void main() async {
  String version = '26.08.19.e.beta';
  String notes = '''🚀 Cập nhật Phiên bản 26.08.19.e.beta

🎉 Tính năng mới:
- Thêm lời chào cá nhân hóa (Xin chào + Tên) và logo ứng dụng tại màn hình chính khi đã đăng nhập.
- Hỗ trợ click chuột phải mở menu cài đặt ngay trong trình phát video (Native Player).
- Thiết kế lại mục lục Cài đặt (Sidebar) đồng nhất với phong cách trong suốt (Glassmorphism) của màn hình chính.
- Việt hóa toàn bộ tooltip, khung tìm kiếm, cài đặt âm thanh, màu sắc, bình luận.

🛠️ Cải tiến & Sửa lỗi:
- Khắc phục lỗi treo Build kéo dài do sai lệch cấu trúc mã nguồn (Bracket mismatches) từ các bản cập nhật cũ.
- Tự động ngắt tự động phát (autoplay) Trailer nếu người dùng bấm vào xem phim trước khi Trailer tải xong.
- Tối ưu hóa lưới hiển thị tập phim (Wrap) để không bị tràn màn hình khi tên tập phim hoặc Torrent/P2P quá dài.
- Hiển thị giá trị mili-giây (ms) chuẩn xác cho các thanh trượt độ trễ âm thanh & phụ đề.
- Sửa lỗi lệch giao diện khối chọn ngôn ngữ và căn chỉnh lại các hộp thoại thả xuống (Dropdown).''';

  final url = Uri.parse('https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/beta');
  final body = {
    "fields": {
      "latest_version": {"stringValue": version},
      "download_url": {"stringValue": "https://github.com/Tien360/mytv4u/releases/download/$version/MyTV4U_Setup_$version.exe"},
      "release_notes": {"stringValue": notes},
      "is_force_update": {"booleanValue": true}
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

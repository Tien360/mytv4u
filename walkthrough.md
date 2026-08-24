# Walkthrough: Tính năng Hiển thị Tiến độ Tập Phim Thông minh (Next Episode Tracker)

## Các thay đổi đã thực hiện
- **Cấu trúc lại bộ Logic "Next Episode"**: Nâng cấp từ hiển thị tĩnh sang cấu trúc 11 kịch bản khác nhau tùy theo vòng đời của phim (First Half, Halfway, Second Half, Penultimate, Finale, Completed).
- **Hỗ trợ Random L10n**: Thêm hàm `L10n.tList` vào `l10n.dart` để lấy ngẫu nhiên một mảng các câu thoại từ file `.json`.
- **Đa dạng hóa ngôn ngữ**: Bổ sung hơn 110 câu thoại sinh động (song ngữ Anh - Việt) vào `vi.json` và `en.json`.
- **Cơ chế Dự đoán và Ân hạn (Grace Period)**: 
  - Dự đoán thời gian phát sóng tập kế tiếp (cộng thêm 7 ngày) nếu tập hôm nay đã chiếu.
  - Thêm khoảng "ân hạn 3 ngày" (3-day grace period) để vinh danh người dùng đã theo dõi tập cuối cùng vừa mới ra lò.

## Kết quả Kiểm thử (Validation)
- Đã chạy `flutter build windows` thành công, không phát hiện lỗi cú pháp.
- Các trường hợp TMDB thiếu dữ liệu (`null` total episodes) được bắt gọn gàng vào kịch bản mặc định bằng `Try-Catch`.

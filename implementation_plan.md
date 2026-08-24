# Kế hoạch Nâng cấp Hiển thị Tiến độ Tập phim (Ver 2.0)

## Kịch bản (Scenarios) & Logic Phân tích

Tôi sẽ định nghĩa một hàm tiện ích mới trong `L10n` (`L10n.tList`) để lấy một mảng các câu thoại ngẫu nhiên từ file ngôn ngữ (`vi.json` / `en.json`), đáp ứng yêu cầu "chuẩn hóa đa ngôn ngữ".

App sẽ tính toán các biến số sau:
- `nextEpNum`: Số tập chuẩn bị chiếu (Từ TMDB).
- `totalEps`: Tổng số tập.
- `currentEpNum`: Số tập mới nhất đã có trên App.
- `diff`: Số ngày đếm ngược (so với hôm nay).
- `isAvailable`: Đã có vietsub/nguồn chưa (`currentEpNum >= nextEpNum`).

Dựa trên các biến này, chia ra **6 kịch bản chính**, mỗi kịch bản có **9-10 câu thoại ngẫu nhiên**:

### 1. Kịch bản Tương lai (Bình thường)
- Áp dụng: `diff > 0` và không phải 2 tập cuối.
- Ví dụ ngẫu nhiên: 
  - "Tập {X} sẽ phát tiếp vào ngày {DATE}. Ráng đợi {DIFF} ngày nữa nhé!"
  - "Chỉ còn {DIFF} ngày nữa là cày tập {X} rồi!"
  - ... (Tổng 10 câu)

### 2. Kịch bản Tương lai (Tập Cận Cuối)
- Áp dụng: `diff > 0` và `nextEpNum == totalEps - 1`.
- Ví dụ ngẫu nhiên:
  - "Chặng đường sắp kết thúc! Tập {X} (kế cuối) sẽ lên sóng vào {DATE}."
  - "Sắp đến hồi kết! Còn {DIFF} ngày nữa để xem tập cận cuối!"
  - ... (Tổng 10 câu)

### 3. Kịch bản Tương lai (Tập Cuối)
- Áp dụng: `diff > 0` và `nextEpNum == totalEps`.
- Ví dụ ngẫu nhiên:
  - "Hành trình chúng ta sắp kết thúc. Tập cuối sẽ lên sóng ngày {DATE}."
  - "Chuẩn bị khăn giấy đi nào! Tập cuối ra mắt sau {DIFF} ngày nữa!"
  - ... (Tổng 10 câu)

### 4. Kịch bản Hôm nay chiếu (Nhưng chưa có / Chờ Mux)
- Áp dụng: `diff == 0` và `!isAvailable`.
- Chia nhỏ (Tập thường / Tập cuối):
  - "Hôm nay chiếu tập {X} bạn nhé, nhưng nguồn đang chờ cập nhật. Kiên nhẫn xíu nha!"
  - "Lịch báo hôm nay có tập {X}, hãy F5 liên tục chờ admin up bài nhé!"
  - Nếu là tập cuối: "Ngày phán xét đến rồi! Đang hóng nguồn up tập cuối!"
  - ... (Tổng 10 câu)

### 5. Kịch bản Hôm nay chiếu (Đã có / Tận hưởng)
- Áp dụng: `diff == 0` và `isAvailable`.
- **Lưu ý về Tập kế tiếp:** Khi tập hôm nay ĐÃ CÓ, TMDB thường chưa cập nhật kịp dữ liệu của tập tiếp theo. Tôi sẽ lập trình một thuật toán **"Dự đoán lịch chiếu"**: Nếu phim chiếu hàng tuần, App sẽ tự cộng thêm 7 ngày; Nếu chiếu hàng ngày, App cộng 1 ngày, để sinh ra câu: 
  - "Hãy tận hưởng tập mới hôm nay nhé! Tập {X+1} dự kiến phát vào {NEXT_DATE}."
  - "Tập {X} đã cập bến! Lên đồ quẩy thôi! Đừng quên lịch tập tiếp theo nhé."
  - Nếu là tập cuối: "Tập cuối đã lên sóng! Cảm ơn bạn đã đồng hành cùng bộ phim."
  - ... (Tổng 10 câu)

### 6. Kịch bản Quá khứ / Đã chiếu
- Áp dụng: `diff < 0` (Thường ít xảy ra do TMDB tự cập nhật, nhưng vẫn chặn lỗi).
- "Tập {X} đã lên sóng (vượt tiến độ {ABS_DIFF} ngày)."

## Các bước code (Proposed Changes)

#### [MODIFY] `lib/utils/l10n.dart`
- Thêm hàm `static List<String> tList(String key)` để hỗ trợ bóc mảng String từ file JSON.

#### [MODIFY] `assets/langs/vi.json` & `en.json`
- Thêm hàng loạt các mảng JSON chứa 10 câu nói cho mỗi kịch bản (Kèm encode các biến `{X}`, `{DATE}`, `{DIFF}`, `{NEXT_DATE}`).

#### [MODIFY] `lib/screens/movie_detail_screen.dart`
- Thêm hàm `_extractCurrentEpisodeNum()` dùng Regex.
- Xây dựng cây IF-ELSE bao phủ 6 kịch bản.
- Thuật toán nội suy `nextDate`: Dựa vào khoảng cách ngày phát của các tập trước đó (nếu có) hoặc mặc định cộng 7 (nếu phim dài tập) để đoán lịch chiếu tiếp theo.

import json

vi_data = {
  "easter_universal": [
    "Bật điều hòa, đắp chăn và thưởng thức thôi!",
    "Pha bắp rang, rót nước và chuẩn bị đắm chìm vào phim nhé!",
    "Lên kèo bắp nước ngay và luôn!",
    "Đã tới giờ xem phim rồi, không phải giờ làm việc!",
    "Phim hay đợi bạn đấy, tắt mọi sđt đi và tập trung nào!",
    "Chuẩn bị khăn giấy phòng khi cảm xúc bị cuốn theo phim nhé!",
    "Rạp chiếu phim tư gia đã sẵn sàng, chỉ còn thiếu bạn thôi!",
    "Tắt hết thông báo rác, phim này xứng đáng có sự chú ý toàn phần!",
    "Gọi hội bạn đến xem chung cho vui nào!",
    "Ngày hôm nay biết làm gì chưa? Xem phim thôi!"
  ],
  "easter_universal_midnight": [
    "Khuya rồi, tắt máy đi ngủ để bảo vệ sức khỏe nhé! 🛏️",
    "Thức đêm hói đầu đấy bạn ơi, đi ngủ lẹ!",
    "Phim hay nhưng sức khỏe quan trọng hơn nha!",
    "Mắt đang mờ rồi, mai xem tiếp cũng không muộn!",
    "Đồng hồ báo sáng vẫn còn đó, liệu hồn rồi ngủ đi!",
    "Admin cũng đã ngủ, bạn cũng nên ngủ thôi!",
    "Bỏ phim vào bộ nhớ đi, sáng mai thoải mái coi tiếp!",
    "Khuya rồi đó nhé, cơ thể cần nghỉ ngơi 8 tiếng mỗi ngày!"
  ],
  "easter_genre_action": [
    "Khói lửa mịt mù, chuẩn bị tinh thần! 💥",
    "Đánh đấm nảy lửa, căng cực căng cực!",
    "Phát súng âm thanh nổi để cảm nhận độ phê nhé!",
    "Bám ghế, cảnh hành động sắp nổ tung!",
    "Anh hùng đã sẵn sàng, chỉ chờ bạn mở phim!",
    "Xe phóng, súng nạp, phi vụ bắt đầu!",
    "Xem mà muốn hô hào thì cứ tự nhiên nhé!",
    "Cảnh chiến này triệu đô mới dựng nổi, trân trọng mà xem nhé!"
  ],
  "easter_genre_romance": [
    "Chuẩn bị khăn giấy đi, cẩu lương ngập mặt! 🥰",
    "Tình yêu màu hồng mộng mơ!",
    "Ngọt lịm tim, đường nhiều quá nha!",
    "Hành trình tình yêu của 2 nhân vật này đang chờ bạn chứng kiến!",
    "Đẩy thuyền, đẩy thuyền, đẩy cho mạnh vào!",
    "Coi phim tình cảm nhớ đừng gọi người yêu cũ nhé!",
    "Phim này đem ra ngày Valentine xem là chuẩn luôn!",
    "Hy vọng bạn cũng có ai đó ngồi cạnh xem cùng ❤"
  ],
  "easter_genre_comedy": [
    "Cười sái quai hàm! 😂",
    "Không nên xem lúc đang nhai cơm!",
    "Giải trí cực mạnh, độ hài đảm bảo!",
    "Phòng khách sắp vang tiếng cười rồi đó!",
    "Lâu rồi mới có bộ phim hài đỉnh như vậy!",
    "Có những phù thủy khiến bạn cười, đó chính là đạo diễn phim này!",
    "Cười nhỏ thôi kẻo phiền hàng xóm đó!",
    "Xem phim này đảm bảo mood tốt cả tuần!"
  ],
  "easter_genre_historical": [
    "Thâm cung bí sử, xuyên không thôi!",
    "Cung đấu căng thẳng, ai sẽ thắng đây?",
    "Phục dựng lịch sử tốn hàng tỷ, màu sắc đẹp tuyệt!",
    "Áo quần cổ trang đẹp mắt lắm, xem mà mê!",
    "Bí ẩn cung đình, tự xem mà cảm nhận!",
    "Tranh giành vương quyền lại bắt đầu, kịch tính từng phút!",
    "Hậu cung ba ngàn giai lệ, ai sẽ giành chiến thắng cuối cùng?"
  ],
  "easter_genre_psychological": [
    "Plot twist lật bàn, nhớ đội mũ bảo hiểm! 🧠",
    "Sang chấn tâm lý cực mạnh, cần hồi phục chưa?",
    "Hack não cực mạnh, ai cũng bị lừa!",
    "Xem phim này xong sẽ khó ngủ vì cứ nghĩ mãi!",
    "Tâm lý phức tạp, nhưng rất thỏa mãn khi hiểu ra!",
    "Nhân vật này thật sự là ai? Bạn có biết không?",
    "Phim tâm lý luôn có thứ gì ẩn giấu phía sau, tin tôi đi!"
  ],
  "easter_genre_crime": [
    "Sự thật chỉ có một! Phá án thôi!",
    "Cảnh sát tới đây, giơ tay lên!",
    "Đấu trí căng não, ai là hung thủ?",
    "Làm thám tử một ngày, bắt tội phạm một giờ!",
    "Phim hình sự hay như này hiếm lắm đó!",
    "Lối đi của kẻ ác đã lộ ra rồi, chỉ cần tìm bằng chứng thôi!",
    "Phim hình sự không bao giờ cũ, chỉ có người xem cũ thôi!"
  ],
  "easter_genre_scifi": [
    "Cánh cổng vũ trụ đã mở! 🚀",
    "Robot xâm lăng hay con người xâm lăng Robot?",
    "Du hành thời gian phức tạp lắm, cẩn thận nghịch lý!",
    "Trí tuệ nhân tạo có cảm xúc thì sao... Xem phim này để biết!",
    "Công nghệ lõi là đây, khoa học đi trước 100 năm!",
    "Người ngoài hành tinh có thông minh hơn chúng ta không?",
    "Phim viễn tưởng đánh thức ước mơ khám phá vũ trụ trong bạn!"
  ],
  "easter_genre_horror": [
    "Đừng nhìn ra sau lưng... 👻",
    "Ma tới kìa!",
    "Xem đêm nhớ trùm mền kín nhé!",
    "Jump scare đầu tiên đến lúc nào, chú ý nhé!",
    "Âm thanh rùng rợn lắm, nhớ mở to lên!",
    "Phim này xem mà cửa nhà khóa chưa?",
    "Nhân vật này sắp chết rồi, ai cũng đoán được mà vẫn sợ!",
    "Ban đêm mà ở nhà một mình thì đừng xem phim này!"
  ],
  "easter_genre_animation": [
    "Về lại tuổi thơ nào! 🌈",
    "Thế giới diệu kỳ đang chờ đón!",
    "Hoạt hình không chỉ dành cho trẻ em đâu nhé!",
    "Ánh sáng màu sắc dễ thương lắm, kĩ xảo tuyệt vời!",
    "Nhân vật hoạt hình luôn có bài học ý nghĩa sau mỗi câu chuyện!",
    "Sự sáng tạo vô bờ bến trong từng khung hình!",
    "Kỳ lân, rồng và cầu vồng đang chờ bạn khám phá!"
  ],
  "easter_genre_lgbt": [
    "Love is love! 🏳️‍🌈",
    "Ngọt ngào quá, đẩy thuyền thôi!",
    "Cầu vồng rực rỡ, tình yêu không giới hạn!",
    "BL/GL, chỉ biết là mê mệt!",
    "Hai người họ tình tứ thế này khó cưỡng quá!",
    "Hội shipper điểm danh, lên thuyền nào!",
    "Phim này làm tôi tin vào tình yêu thực sự!",
    "Màu cầu vồng đẹp quá, như bộ phim này vậy!"
  ],
  "easter_progress_party": [
    "Tập mới vừa thổi vừa xơi ngay nào! 🔥",
    "Đợi mãi mới ra, cày lẹ kẻo bị spoil!",
    "Admin đã upload xong, còn đợi gì nữa?",
    "Tập mới nóng hổi! Nhanh vào xem đi!",
    "Thức đợi mãi tập mới, cuối cùng cũng ra rồi!",
    "Ăn mừng nào, tập mới đã có mặt!"
  ],
  "easter_progress_cry": [
    "Chưa gì đã hết phim... 😭",
    "Sẽ nhớ các nhân vật lắm đây!",
    "Tạm biệt bộ phim tuyệt vời, đã đồng hành cùng nhau một quãng thời gian!",
    "Chia tay nhân vật thật sự lưu luyến!",
    "Xem xong vẫn không dứt ra được... Phim hay thật!",
    "Mong rằng sẽ có mùa tiếp theo..."
  ],
  "easter_progress_rage": [
    "Đang hối Admin vắt giò lên cổ Mux! Chờ xíu nhé!",
    "Admin đang bận úp mì tôm, từ từ sẽ có phim!",
    "Phần mềm đang render, kiên nhẫn chút nhé!",
    "Tập mới đã chiếu trên TV nhưng App chưa có, ráng đợi một chút!",
    "Hãy kiên nhẫn! Admin đang làm việc với tốc độ bàn thờ!",
    "Hạ hỏa, hạ hỏa, phim sắp có rồi!"
  ],
  "easter_progress_chill": [
    "Chặng đường còn dài, cứ thong thả chill và tận hưởng nhé 🥤",
    "Phim nhiều tập đảm bảo giải trí dài dài!",
    "Có nhiều thời gian, hãy thưởng thức từng tập thật chậm!",
    "Phần mở đầu lôi cuốn, càng về sau càng hấp dẫn!",
    "Không cần vội, phim vẫn còn đó chứ không đi đâu mất!"
  ],
  "easter_progress_tense": [
    "Drama đang căng, hồi hộp chờ xem tuần sau giải quyết ân oán thế nào! 😱",
    "Gần cuối rồi, mọi bí mật sắp được hé lộ!",
    "Nút thắt đang tới đỉnh điểm, không thể rời mắt!",
    "Cắn móng tay hồi hộp xem phe nào thắng!",
    "Ai sẽ sống sót đến cuối phim đây?",
    "Plot twist chưa ra hết đâu, còn nhiều bất ngờ phía trước!"
  ],
  "easter_eggs_title": "Hiệu ứng Tương tác (Easter Eggs)",
  "easter_eggs_toggle": "Bật Hiệu ứng Trứng Phục Sinh",
  "easter_eggs_desc": "Nhấn vào dòng trạng thái tập mới ở mỗi phim để quay thưởng hiệu ứng! Có 4 bậc từ Phổ thông đến Huyền thoại (tỉ lệ 1%). Chúc bạn may mắn!"
}

with open("assets/langs/vi.json", "r", encoding="utf-8") as f:
    vi = json.load(f)

vi.update(vi_data)

with open("assets/langs/vi.json", "w", encoding="utf-8") as f:
    json.dump(vi, f, ensure_ascii=False, indent=2)

print("Updated Vietnamese strings with proper accents.")

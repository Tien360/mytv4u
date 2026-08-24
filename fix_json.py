import json
import os

vi_path = "assets/langs/vi.json"
en_path = "assets/langs/en.json"

vi_keys = {
    "ep_msg_future_normal": [
        "Tập {X} sẽ phát tiếp vào ngày {DATE}. Ráng đợi {DIFF} ngày nữa nhé!",
        "Chỉ còn {DIFF} ngày nữa là được cày tập {X} rồi!",
        "Sắp ra mắt tập {X} sau {DIFF} ngày. Hóng quá đi!",
        "Đánh dấu lịch ngày {DATE} nhé, tập {X} sắp lên sóng!",
        "Còn {DIFF} ngày nữa. Đếm ngược tới tập {X} nào!",
        "Đừng quên lịch hẹn ngày {DATE} cho tập {X} nhé!",
        "Tập {X} đang được chuẩn bị, {DIFF} ngày nữa sẽ gặp lại bạn!",
        "Háo hức quá! Tập {X} sẽ lên sóng vào {DATE}.",
        "Ghi chú lại ngày {DATE} nhé, tập {X} sắp ra mắt rồi!",
        "Ráng nhịn thêm {DIFF} ngày nữa để xem tập {X} nha!"
    ],
    "ep_msg_future_halfway": [
        "Ta đã đi được nửa chặng đường cùng nhau. Tập {X} sẽ phát vào {DATE}.",
        "Phim đã đi được một nửa rồi! Cùng chờ đón tập {X} sau {DIFF} ngày nhé.",
        "Nửa chặng đường đã qua, kịch tính bùng nổ ở tập {X} vào {DATE}!",
        "Hành trình đã qua phân nửa. Cùng đón xem tập {X} vào {DATE} nha.",
        "Đã xem được nửa bộ rồi đấy! Tập {X} sẽ lên sóng sau {DIFF} ngày.",
        "Nửa đường rồi, tiếp tục đồng hành cùng tập {X} vào {DATE} nhé!",
        "Chặng đường tiếp theo bắt đầu với tập {X} vào ngày {DATE}.",
        "Cùng bước sang nửa sau của bộ phim ở tập {X} vào {DATE} nhé!",
        "Mọi thứ mới chỉ bắt đầu hấp dẫn hơn từ tập {X}, đón xem vào {DATE}!",
        "Nửa cuối phim hứa hẹn sẽ bùng nổ. Tập {X} ra mắt sau {DIFF} ngày nữa!"
    ],
    "ep_msg_future_penultimate": [
        "Chặng đường sắp kết thúc! Tập {X} (kế cuối) sẽ lên sóng vào {DATE}.",
        "Sắp đến hồi kết! Còn {DIFF} ngày nữa để xem tập cận cuối!",
        "Chỉ còn 1 bước nữa là đến đại kết cục. Chờ tập {X} vào {DATE} nhé.",
        "Hồi hộp quá! Tập áp chót {X} sẽ phát sóng sau {DIFF} ngày.",
        "Mọi nút thắt chuẩn bị được gỡ ở tập {X} vào ngày {DATE}!",
        "Gần tới đích rồi! Tập kế cuối {X} sẽ lên sóng vào {DATE}.",
        "Sẵn sàng cho tập áp chót chưa? Tập {X} ra mắt sau {DIFF} ngày nữa!",
        "Bầu không khí đang nóng lên, tập {X} lên sóng ngày {DATE}!",
        "Đừng bỏ lỡ tập {X} (kế cuối) vào ngày {DATE} nhé!",
        "Câu chuyện sắp đi đến hồi kết. Ráng đợi {DIFF} ngày cho tập {X} nha!"
    ],
    "ep_msg_future_finale": [
        "Hành trình chúng ta sắp kết thúc. Tập cuối sẽ lên sóng ngày {DATE}.",
        "Chuẩn bị khăn giấy đi nào! Tập cuối ra mắt sau {DIFF} ngày nữa!",
        "Đại kết cục sắp tới! Hãy chờ đón tập cuối vào {DATE}.",
        "Trùm cuối sắp xuất hiện. Cùng xem tập cuối vào {DATE} nhé!",
        "Ngày chia tay sắp đến. Tập cuối sẽ phát sóng sau {DIFF} ngày.",
        "Mọi câu hỏi sẽ được giải đáp ở tập cuối vào ngày {DATE}.",
        "Bạn đã sẵn sàng cho tập cuối chưa? Ráng đợi {DIFF} ngày nữa nha!",
        "Đoạn kết của hành trình. Tập cuối lên sóng vào {DATE}.",
        "Thời khắc quyết định đã tới. Chờ tập cuối vào {DATE} nhé!",
        "Cảm ơn đã đồng hành. Tập cuối cùng sẽ ra mắt sau {DIFF} ngày!"
    ],
    "ep_msg_today_pending": [
        "Hôm nay chiếu tập {X} bạn nhé, đang hóng nguồn cập nhật. Kiên nhẫn xíu nha!",
        "Lịch báo hôm nay có tập {X}, hãy F5 chờ admin up bài nhé!",
        "Tập {X} đã phát sóng hôm nay! Đang chờ Mux vietsub, quay lại sau nha bạn.",
        "Hôm nay có tập {X} nè, ráng đợi phim lên kệ nhé!",
        "Tập {X} đang được chuẩn bị lên sóng trong hôm nay!",
        "Sắp có tập {X} rồi, hóng admin cập nhật nhé!",
        "Tập {X} sẽ có trong hôm nay, chuẩn bị bỏng ngô đi nào!",
        "Đang render tập {X} mới nhất của hôm nay, bạn chờ xíu nha!",
        "Nguồn phim đang tải tập {X}, sắp có để cày rồi!",
        "Hôm nay chiếu tập {X} rồi, quay lại đây sau ít phút nhé!"
    ],
    "ep_msg_today_pending_finale": [
        "Hôm nay chiếu tập cuối! Đang hóng nguồn cập nhật, hồi hộp quá!",
        "Ngày phán xét đến rồi! Đang chờ Mux vietsub tập cuối!",
        "Tập cuối lên sóng hôm nay, admin đang tăng tốc cập nhật, ráng chờ nha!",
        "Hôm nay chia tay bộ phim ở tập cuối, chờ nguồn lên sóng nhé!",
        "Tập cuối đang được chuẩn bị trong hôm nay, hóng quá đi mất!"
    ],
    "ep_msg_today_available": [
        "Hãy tận hưởng tập {X} mới nhất hôm nay nhé! {NEXT_INFO}",
        "Tập {X} đã cập bến! Lên đồ quẩy thôi! {NEXT_INFO}",
        "Tin vui: Tập {X} đã có sẵn. Chúc bạn xem vui vẻ! {NEXT_INFO}",
        "Hàng nóng tập {X} đã về! Tận hưởng ngay nào! {NEXT_INFO}",
        "Tập {X} nóng hổi vừa thổi vừa xem. {NEXT_INFO}",
        "Không phải đợi nữa, tập {X} đã lên sóng. Quẩy thôi! {NEXT_INFO}",
        "Tập {X} đã sẵn sàng phục vụ bạn. Chúc xem vui vẻ! {NEXT_INFO}",
        "Đã có tập {X} rồi đấy, mau vào xem thôi! {NEXT_INFO}",
        "Tập {X} đã cập nhật xong, tận hưởng khoảnh khắc này nhé! {NEXT_INFO}",
        "Thưởng thức tập {X} ngay thôi nào! {NEXT_INFO}"
    ],
    "ep_msg_today_available_finale": [
        "Tập cuối đã lên sóng! Cảm ơn bạn đã đồng hành cùng bộ phim.",
        "Hành trình đã khép lại ở tập cuối. Chúc bạn xem vui vẻ!",
        "Đại kết cục đã có mặt. Tận hưởng tập cuối cùng này nhé!",
        "Tập cuối đã cập bến. Chuẩn bị khăn giấy và xem thôi!",
        "Cảm ơn vì đã đi đến tập cuối cùng. Tận hưởng nhé!"
    ],
    "ep_msg_completed_movie": [
        "Chúc bạn xem phim vui vẻ!",
        "Hãy thư giãn và tận hưởng bộ phim này nhé.",
        "Bỏng ngô đã sẵn sàng chưa? Bắt đầu xem thôi!",
        "Một bộ phim tuyệt vời đang chờ bạn. Tận hưởng nhé!",
        "Dành chút thời gian thư giãn với bộ phim này nào."
    ],
    "ep_msg_completed_short": [
        "Phim đã ra mắt trọn bộ, chúc bạn cày phim vui vẻ!",
        "Bộ phim đã hoàn tất, không cần phải đợi chờ từng tập nữa!",
        "Tất cả các tập đã sẵn sàng, hãy thưởng thức ngay nhé.",
        "Phim đã full bộ, rảnh rỗi cày một lèo luôn nha!",
        "Đã đủ các tập rồi, chúc bạn có những giây phút thư giãn."
    ],
    "ep_msg_completed_long": [
        "Đừng cày hết cả bộ một đêm nhé, giữ sức khỏe để mai còn đi làm!",
        "Phim dài lắm đấy, nhớ nghỉ ngơi hợp lý khi cày trọn bộ nhé.",
        "Hành trình dài đã hoàn tất! Xem từ từ thôi kẻo hại mắt nha.",
        "Cảm ơn bạn đã đồng hành cả chặng đường dài. Chúc bạn cày trọn bộ vui vẻ!",
        "Phim đã Full rồi. Rất hay nhưng sức khỏe là trên hết, đừng thức khuya cày nhé!",
        "Bộ phim dài này đã trọn vẹn, hãy từ từ thưởng thức từng tập nha.",
        "Phim Full rồi! Dành mỗi ngày một ít để thưởng thức cho trọn vẹn nhé.",
        "Một chặng đường dài đã khép lại. Chúc bạn tận hưởng bộ phim tuyệt vời này.",
        "Phim dài đấy, chuẩn bị đồ ăn vặt và xem từ từ thôi nhé!",
        "Đừng cày thâu đêm nhé bạn ơi, phim còn đó chứ không mất đâu!"
    ],
    "ep_msg_past_missed": [
        "Tập {X} đã lên sóng (lệch tiến độ {DIFF} ngày).",
        "Tập {X} đã chiếu trên TV nhưng app chưa cập nhật, kiên nhẫn chút nhé."
    ],
    "ep_msg_next_estimated": "Dự kiến lịch chiếu tập kế tiếp vào khoảng {DATE}.",
    "ep_msg_next_unknown": "Lịch phát tập kế tiếp sẽ sớm được cập nhật."
}

en_keys = {
    "ep_msg_future_normal": [
        "Episode {X} will air on {DATE}. Just {DIFF} more days to wait!",
        "Only {DIFF} days left until episode {X}!",
        "Episode {X} is coming in {DIFF} days. So excited!",
        "Mark your calendar on {DATE} for episode {X}!",
        "{DIFF} days countdown to episode {X}!",
        "Don't forget the date {DATE} for episode {X}!",
        "Episode {X} is in preparation, see you in {DIFF} days!",
        "Can't wait! Episode {X} airs on {DATE}.",
        "Save the date {DATE}, episode {X} is coming soon!",
        "Hold on for {DIFF} more days to watch episode {X}!"
    ],
    "ep_msg_future_halfway": [
        "We're halfway through! Episode {X} airs on {DATE}.",
        "Half of the journey is over! Episode {X} is coming in {DIFF} days.",
        "The halfway mark! Tension rises in episode {X} on {DATE}!",
        "Halfway done. Let's watch episode {X} on {DATE}.",
        "Already halfway! Episode {X} airs in {DIFF} days.",
        "Mid-season approaching, keep going with episode {X} on {DATE}!",
        "The next half starts with episode {X} on {DATE}.",
        "Entering the second half with episode {X} on {DATE}!",
        "Things get more exciting from episode {X}, coming {DATE}!",
        "The second half promises to be explosive. Episode {X} in {DIFF} days!"
    ],
    "ep_msg_future_penultimate": [
        "The journey is almost over! Penultimate episode {X} airs on {DATE}.",
        "Approaching the finale! {DIFF} days left for the penultimate episode!",
        "Just one step to the end. Wait for episode {X} on {DATE}.",
        "So thrilling! Penultimate episode {X} airs in {DIFF} days.",
        "The climax is near in episode {X} on {DATE}!",
        "Almost there! Penultimate episode {X} airs on {DATE}.",
        "Ready for the semi-finale? Episode {X} comes in {DIFF} days!",
        "The heat is on, episode {X} airs {DATE}!",
        "Don't miss the penultimate episode {X} on {DATE}!",
        "The story is wrapping up. Wait {DIFF} days for episode {X}!"
    ],
    "ep_msg_future_finale": [
        "Our journey is ending. The finale airs on {DATE}.",
        "Get your tissues ready! The finale is coming in {DIFF} days!",
        "The grand finale is near! Watch it on {DATE}.",
        "The final boss approaches. Watch the finale on {DATE}!",
        "Time to say goodbye. The finale airs in {DIFF} days.",
        "All questions answered in the finale on {DATE}.",
        "Are you ready for the finale? Wait {DIFF} more days!",
        "The end of the road. The finale airs {DATE}.",
        "The deciding moment is here. Wait for the finale on {DATE}!",
        "Thanks for watching. The final episode comes in {DIFF} days!"
    ],
    "ep_msg_today_pending": [
        "Episode {X} airs today! Waiting for the source to update. Be patient!",
        "Episode {X} is scheduled today, refresh to see if admin uploaded it!",
        "Episode {X} aired today! Waiting for subs, check back later.",
        "Episode {X} is coming today, hold on!",
        "Episode {X} is being prepared today!",
        "Episode {X} is almost here, wait for the update!",
        "Episode {X} will be available today, grab your popcorn!",
        "Rendering the latest episode {X} today, wait a moment!",
        "Source is downloading episode {X}, ready soon!",
        "Episode {X} aired today, come back in a few minutes!"
    ],
    "ep_msg_today_pending_finale": [
        "The finale airs today! Waiting for the source to update, so thrilling!",
        "Judgment day is here! Waiting for the finale subs!",
        "Finale airs today, admin is working fast, please hold on!",
        "Saying goodbye today in the finale, wait for the source!",
        "The finale is being prepared today, can't wait!"
    ],
    "ep_msg_today_available": [
        "Enjoy the new episode {X} today! {NEXT_INFO}",
        "Episode {X} has arrived! Let's watch! {NEXT_INFO}",
        "Good news: Episode {X} is available. Enjoy! {NEXT_INFO}",
        "Hot episode {X} is here! Enjoy it now! {NEXT_INFO}",
        "Episode {X} is fresh out of the oven. {NEXT_INFO}",
        "No more waiting, episode {X} is live. Let's go! {NEXT_INFO}",
        "Episode {X} is ready for you. Happy watching! {NEXT_INFO}",
        "Episode {X} is available, dive in now! {NEXT_INFO}",
        "Episode {X} updated, enjoy this moment! {NEXT_INFO}",
        "Watch episode {X} right now! {NEXT_INFO}"
    ],
    "ep_msg_today_available_finale": [
        "The finale is live! Thank you for accompanying this series.",
        "The journey concludes with the finale. Enjoy!",
        "The grand finale is here. Enjoy this final episode!",
        "The finale has arrived. Get your tissues and watch!",
        "Thanks for making it to the final episode. Enjoy!"
    ],
    "ep_msg_completed_movie": [
        "Enjoy the movie!",
        "Relax and enjoy this film.",
        "Popcorn ready? Let's start watching!",
        "A great movie awaits you. Enjoy!",
        "Take some time to relax with this movie."
    ],
    "ep_msg_completed_short": [
        "The full series is out, happy binge-watching!",
        "The series is complete, no more waiting for episodes!",
        "All episodes are ready, enjoy them now.",
        "Full series available, binge it all in one go!",
        "All episodes are here, wishing you a relaxing time."
    ],
    "ep_msg_completed_long": [
        "Don't binge the whole thing in one night, save your health for work!",
        "It's a long series, remember to take breaks while binge-watching.",
        "The long journey is complete! Watch slowly to protect your eyes.",
        "Thanks for sticking around for the long run. Happy binge-watching!",
        "The series is full. Health first, don't stay up too late!",
        "This long series is complete, take your time to enjoy each episode.",
        "Full series out! Watch a little every day to fully enjoy it.",
        "A long journey has closed. Enjoy this amazing series.",
        "It's a long one, grab snacks and watch slowly!",
        "Don't pull an all-nighter, the series isn't going anywhere!"
    ],
    "ep_msg_past_missed": [
        "Episode {X} aired (delayed {DIFF} days).",
        "Episode {X} aired on TV but the app hasn't updated, be patient."
    ],
    "ep_msg_next_estimated": "Next episode is estimated to air around {DATE}.",
    "ep_msg_next_unknown": "Schedule for the next episode will be updated soon."
}

def update_lang(path, keys_to_add):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {}
    
    for k, v in keys_to_add.items():
        data[k] = v
        
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Updated {path}")

update_lang(vi_path, vi_keys)
update_lang(en_path, en_keys)

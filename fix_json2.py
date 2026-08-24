import json
import os

vi_path = "assets/langs/vi.json"
en_path = "assets/langs/en.json"

vi_keys = {
    "ep_msg_future_first_half": [
        "Kịch tính mới chỉ bắt đầu! Tập {X} sẽ ra mắt vào {DATE}, ráng đợi {DIFF} ngày nữa nhé.",
        "Càng xem càng cuốn! Đừng bỏ lỡ diễn biến tiếp theo ở tập {X} sau {DIFF} ngày nữa.",
        "Câu chuyện vừa mở màn đã rất hấp dẫn. Chờ tập {X} vào {DATE} nhé!",
        "Chỉ còn {DIFF} ngày nữa là được cày tập {X} rồi!",
        "Hóng quá đi! Đánh dấu lịch ngày {DATE} cho tập {X} nhé.",
        "Mọi thứ mới chỉ bắt đầu. Còn {DIFF} ngày nữa, đếm ngược tới tập {X} nào!",
        "Tập {X} đang được chuẩn bị, {DIFF} ngày nữa sẽ gặp lại bạn!",
        "Đừng quên lịch hẹn ngày {DATE} để theo dõi tập {X} nhé!",
        "Mới những tập đầu mà đã cuốn thế này! Ráng đợi {DIFF} ngày để xem tập {X}.",
        "Câu chuyện đang mở ra nhiều bí ẩn. Tập {X} sẽ lên sóng vào {DATE}."
    ],
    "ep_msg_future_halfway": [
        "Ta đã đi được nửa chặng đường cùng nhau! Tập {X} (giữa mùa) sẽ phát vào {DATE}.",
        "Phim đã đi được một nửa rồi! Cùng chờ đón tập {X} sau {DIFF} ngày nhé.",
        "Nửa chặng đường đã qua, kịch tính bùng nổ ở tập {X} vào {DATE}!",
        "Hành trình đã qua phân nửa. Cùng đón xem tập {X} vào {DATE} nha.",
        "Đã xem được nửa bộ rồi đấy! Tập {X} sẽ lên sóng sau {DIFF} ngày.",
        "Nửa đường rồi, tiếp tục đồng hành cùng tập {X} vào {DATE} nhé!",
        "Chặng đường tiếp theo bắt đầu với tập {X} vào ngày {DATE}.",
        "Cùng bước sang nửa sau của bộ phim ở tập {X} vào {DATE} nhé!",
        "Đã được 50% chặng đường. Tập {X} ra mắt sau {DIFF} ngày nữa!",
        "Cột mốc giữa mùa! Đón xem tập {X} vào ngày {DATE} nhé."
    ],
    "ep_msg_future_second_half": [
        "Ta đã đi hơn nửa chặng đường! Mọi thứ đang dần sáng tỏ ở tập {X} vào {DATE}.",
        "Chặng đường đang ngắn lại, kịch tính dâng cao. Cùng hóng tập {X} sau {DIFF} ngày nhé!",
        "Càng về cuối càng hấp dẫn! Tập {X} sẽ lên sóng vào ngày {DATE}.",
        "Nút thắt đang dần được gỡ. Chờ tập {X} sau {DIFF} ngày nữa nhé!",
        "Gần tới đích rồi! Cùng đếm ngược {DIFF} ngày cho tập {X}.",
        "Mọi bí mật sắp được bật mí. Tập {X} lên sóng ngày {DATE}!",
        "Cuộc chơi ngày càng gay cấn. Đừng bỏ lỡ tập {X} vào {DATE} nha.",
        "Chỉ còn vài tập nữa thôi! Tập {X} sẽ phát sóng sau {DIFF} ngày.",
        "Đã đi hơn phân nửa hành trình. Cùng xem tiếp tập {X} vào {DATE}!",
        "Những diễn biến quan trọng nhất đang tới. Ráng đợi {DIFF} ngày cho tập {X}!"
    ],
    "ep_msg_future_penultimate": [
        "Chặng đường sắp kết thúc! Tập {X} (kế cuối) sẽ lên sóng vào {DATE}.",
        "Chỉ còn một bước nữa là đến hồi kết! Tập {X} ra mắt sau {DIFF} ngày.",
        "Sắp đến đại kết cục! Còn {DIFF} ngày nữa để xem tập cận cuối!",
        "Hồi hộp quá! Tập áp chót {X} sẽ phát sóng vào {DATE}.",
        "Mọi nút thắt chuẩn bị được gỡ ở tập {X} vào ngày {DATE}!",
        "Gần tới đích rồi! Tập kế cuối {X} sẽ lên sóng vào {DATE}.",
        "Sẵn sàng cho tập áp chót chưa? Ráng đợi {DIFF} ngày nữa nhé!",
        "Bầu không khí đang nóng nhất. Đừng bỏ lỡ tập {X} (kế cuối) vào {DATE}!",
        "Tập bản lề trước khi kết thúc! Cùng đếm ngược {DIFF} ngày nào.",
        "Câu chuyện sắp khép lại. Ráng đợi tập kế cuối {X} vào ngày {DATE} nha!"
    ],
    "ep_msg_future_finale": [
        "Hành trình chúng ta sắp kết thúc. Tập cuối sẽ lên sóng ngày {DATE}. Chuẩn bị khăn giấy đi nào!",
        "Đại kết cục sắp tới! Tập cuối ra mắt sau {DIFF} ngày nữa!",
        "Ngày chia tay sắp đến. Tập cuối cùng sẽ phát sóng vào {DATE}.",
        "Mọi câu hỏi sẽ được giải đáp ở tập cuối vào ngày {DATE}.",
        "Trùm cuối sắp xuất hiện! Cùng xem tập cuối vào {DATE} nhé.",
        "Bạn đã sẵn sàng cho tập cuối chưa? Ráng đợi {DIFF} ngày nữa nha!",
        "Đoạn kết của hành trình. Tập cuối lên sóng sau {DIFF} ngày.",
        "Thời khắc quyết định đã tới. Đánh dấu ngày {DATE} cho tập cuối nhé!",
        "Đã đến lúc khép lại câu chuyện. Tập cuối sẽ có mặt vào {DATE}.",
        "Cùng đếm ngược {DIFF} ngày để xem cái kết trọn vẹn của bộ phim nhé!"
    ],
    "ep_msg_today_pending": [
        "Hôm nay chiếu tập {X} bạn nhé, nhưng nguồn đang chờ cập nhật. Kiên nhẫn xíu nha!",
        "Lịch báo hôm nay có tập {X}, hãy F5 liên tục chờ admin up bài nhé!",
        "Tập {X} đang được chiếu trên TV hôm nay! Chờ Mux vietsub, quay lại sau nha bạn.",
        "Hôm nay có tập {X} nè, ráng đợi phim lên kệ nhé!",
        "Tập {X} đang được chuẩn bị lên sóng trong hôm nay!",
        "Sắp có tập {X} rồi, hóng admin cập nhật nhé!",
        "Tập {X} sẽ có trong hôm nay, chuẩn bị bỏng ngô đi nào!",
        "Đang render tập {X} mới nhất của hôm nay, bạn chờ xíu nha!",
        "Nguồn phim đang tải tập {X}, sắp có để cày rồi!",
        "Hôm nay chiếu tập {X} rồi, quay lại đây sau ít phút nhé!"
    ],
    "ep_msg_today_pending_finale": [
        "Hôm nay chiếu tập cuối! Ngày phán xét đến rồi, ráng đợi admin Mux nhé...",
        "Tập cuối cùng đang lên sóng TV hôm nay! Hồi hộp quá, chờ nguồn cập nhật xíu nha bạn!",
        "Ngày chia tay đến rồi! Đang chờ Mux vietsub tập cuối!",
        "Tập cuối lên sóng hôm nay, admin đang tăng tốc cập nhật, ráng chờ nha!",
        "Tập cuối đang được chuẩn bị trong hôm nay, hóng quá đi mất!"
    ],
    "ep_msg_today_available": [
        "Hãy tận hưởng tập {X} mới hôm nay nhé! {NEXT_INFO}",
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
    "ep_msg_just_finished_finale": [
        "Tập cuối đã lên sóng! Cảm ơn bạn đã đồng hành cả chặng đường dài.",
        "Một chặng đường đã khép lại trọn vẹn. Chúc bạn thưởng thức tập cuối thật cảm xúc!",
        "Cảm ơn vì đã đi đến tập cuối cùng. Tận hưởng đại kết cục nhé!",
        "Hành trình đã khép lại ở tập cuối. Chúc bạn xem vui vẻ!",
        "Đại kết cục đã có mặt. Cảm ơn bạn đã luôn theo dõi và ủng hộ bộ phim!",
        "Tập cuối đã cập bến. Chuẩn bị khăn giấy và xem thôi!",
        "Tạm biệt bộ phim tuyệt vời. Cảm ơn bạn đã đồng hành cùng chúng tôi!",
        "Khoảnh khắc chia tay đã đến. Chúc bạn có những phút giây trọn vẹn với tập cuối.",
        "Phim đã kết thúc viên mãn. Rất vui vì được đồng hành cùng bạn!",
        "Tập cuối cùng đây rồi! Cảm ơn bạn đã đi hết chặng đường dài này."
    ],
    "ep_msg_completed_short": [
        "Phim đã ra mắt trọn bộ, hãy thư giãn và thưởng thức nhé.",
        "Bộ phim đã hoàn tất, không cần phải đợi chờ từng tập nữa!",
        "Tất cả các tập đã sẵn sàng, chúc bạn xem phim vui vẻ.",
        "Phim đã full bộ, rảnh rỗi cày một lèo luôn nha!",
        "Đã đủ các tập rồi, chúc bạn có những giây phút thư giãn.",
        "Chúc bạn xem phim vui vẻ!",
        "Hãy thư giãn và tận hưởng bộ phim này nhé.",
        "Bỏng ngô đã sẵn sàng chưa? Bắt đầu xem thôi!",
        "Một bộ phim tuyệt vời đang chờ bạn. Tận hưởng nhé!",
        "Dành chút thời gian thư giãn với bộ phim này nào."
    ],
    "ep_msg_completed_long": [
        "Đừng cày hết cả bộ một đêm nhé, giữ sức khỏe để mai còn đi làm!",
        "Phim đã Full rồi. Rất hay nhưng sức khỏe là trên hết, đừng thức khuya cày nhé!",
        "Hành trình dài đã hoàn tất! Xem từ từ thôi kẻo hại mắt nha bạn.",
        "Phim dài lắm đấy, nhớ nghỉ ngơi hợp lý khi cày trọn bộ nhé.",
        "Bộ phim dài này đã trọn vẹn, hãy từ từ thưởng thức từng tập nha.",
        "Phim Full rồi! Dành mỗi ngày một ít để thưởng thức cho trọn vẹn nhé.",
        "Một bộ phim đồ sộ đã khép lại. Chúc bạn tận hưởng từ từ thật vui vẻ.",
        "Phim dài đấy, chuẩn bị đồ ăn vặt và xem từ từ thôi nhé!",
        "Đừng cày thâu đêm nhé bạn ơi, phim còn đó chứ không mất đâu!",
        "Chúc bạn cày trọn bộ vui vẻ, nhưng nhớ ngủ đủ giấc nhé!"
    ],
    "ep_msg_past_missed": [
        "Tập {X} đã lên sóng (lệch tiến độ {DIFF} ngày).",
        "Tập {X} đã chiếu trên TV nhưng app chưa cập nhật, kiên nhẫn chút nhé."
    ],
    "ep_msg_next_estimated": "Lịch tập {X} dự kiến vào {DATE}.",
    "ep_msg_next_unknown": "Lịch tập kế tiếp sẽ sớm được cập nhật."
}

en_keys = {
    "ep_msg_future_first_half": [
        "The drama is just beginning! Episode {X} airs on {DATE}, hold on for {DIFF} days.",
        "It's getting addictive! Don't miss episode {X} in {DIFF} days.",
        "The story is so engaging already. Wait for episode {X} on {DATE}!",
        "Only {DIFF} days left to binge episode {X}!",
        "So excited! Mark your calendar for {DATE} for episode {X}.",
        "Things are just starting. {DIFF} days countdown to episode {X}!",
        "Episode {X} is being prepared, see you in {DIFF} days!",
        "Don't forget your date on {DATE} to watch episode {X}!",
        "Such a great start! Hold on for {DIFF} days for episode {X}.",
        "The mysteries are unfolding. Episode {X} airs on {DATE}."
    ],
    "ep_msg_future_halfway": [
        "We've reached the halfway mark! Episode {X} (mid-season) airs on {DATE}.",
        "Half of the journey is over! Await episode {X} in {DIFF} days.",
        "Halfway done, tensions rise in episode {X} on {DATE}!",
        "The journey is half over. Let's watch episode {X} on {DATE}.",
        "Already halfway through! Episode {X} airs in {DIFF} days.",
        "Mid-season is here, keep going with episode {X} on {DATE}!",
        "The next half begins with episode {X} on {DATE}.",
        "Entering the second half with episode {X} on {DATE}!",
        "50% completed. Episode {X} comes out in {DIFF} days!",
        "Mid-season milestone! Watch episode {X} on {DATE}."
    ],
    "ep_msg_future_second_half": [
        "We're past the halfway mark! Things become clearer in episode {X} on {DATE}.",
        "The journey gets shorter, tensions get higher. Await episode {X} in {DIFF} days!",
        "It gets better towards the end! Episode {X} airs on {DATE}.",
        "The knots are untangling. Wait for episode {X} in {DIFF} days!",
        "Almost at the finish line! Counting down {DIFF} days for episode {X}.",
        "Secrets will be revealed. Episode {X} airs on {DATE}!",
        "The game is getting intense. Don't miss episode {X} on {DATE}.",
        "Just a few episodes left! Episode {X} airs in {DIFF} days.",
        "More than half done. Let's watch episode {X} on {DATE}!",
        "The most important events are coming. Wait {DIFF} days for episode {X}!"
    ],
    "ep_msg_future_penultimate": [
        "The journey is almost over! Penultimate episode {X} airs on {DATE}.",
        "Just one step to the finale! Episode {X} comes in {DIFF} days.",
        "Approaching the grand finale! {DIFF} days left for the penultimate episode!",
        "So thrilling! Penultimate episode {X} airs on {DATE}.",
        "All knots will be undone in episode {X} on {DATE}!",
        "Almost there! Penultimate episode {X} airs on {DATE}.",
        "Ready for the semi-finale? Wait {DIFF} more days!",
        "The heat is at its peak. Don't miss episode {X} (penultimate) on {DATE}!",
        "The pivotal episode before the end! Counting down {DIFF} days.",
        "The story is wrapping up. Wait for penultimate episode {X} on {DATE}!"
    ],
    "ep_msg_future_finale": [
        "Our journey is ending. The finale airs on {DATE}. Get your tissues ready!",
        "The grand finale is near! Watch it in {DIFF} days!",
        "Time to say goodbye. The final episode airs on {DATE}.",
        "All questions answered in the finale on {DATE}.",
        "The final boss approaches! Let's watch the finale on {DATE}.",
        "Are you ready for the finale? Wait {DIFF} more days!",
        "The end of the road. The finale airs in {DIFF} days.",
        "The deciding moment is here. Mark {DATE} for the finale!",
        "Time to wrap up the story. The finale arrives on {DATE}.",
        "Counting down {DIFF} days to see the perfect ending of the series!"
    ],
    "ep_msg_today_pending": [
        "Episode {X} airs today! Waiting for the source to update. Be patient!",
        "Episode {X} is scheduled today, keep refreshing for the update!",
        "Episode {X} is airing on TV today! Waiting for subs, check back later.",
        "Episode {X} is coming today, hold on!",
        "Episode {X} is being prepared today!",
        "Episode {X} is almost here, wait for the admin to update!",
        "Episode {X} will be available today, grab your popcorn!",
        "Rendering the latest episode {X} today, wait a moment!",
        "Source is downloading episode {X}, ready soon!",
        "Episode {X} aired today, come back in a few minutes!"
    ],
    "ep_msg_today_pending_finale": [
        "The finale airs today! Judgment day is here, waiting for the subs...",
        "The final episode is airing on TV today! So thrilling, wait for the update!",
        "Saying goodbye today! Waiting for the finale subs!",
        "Finale airs today, admin is working fast, please hold on!",
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
    "ep_msg_just_finished_finale": [
        "The finale is live! Thank you for accompanying this series all the way.",
        "The journey concludes beautifully. Enjoy this emotional finale!",
        "Thanks for making it to the final episode. Enjoy the grand finale!",
        "The journey ends at the finale. Happy watching!",
        "The grand finale is here. Thank you for always watching and supporting!",
        "The finale has arrived. Get your tissues and watch!",
        "Goodbye to an amazing series. Thanks for staying with us!",
        "The moment of parting has come. Enjoy the final episode to the fullest.",
        "The series has concluded nicely. Glad to have you with us!",
        "Here is the final episode! Thanks for sticking through this long journey."
    ],
    "ep_msg_completed_short": [
        "The full series is out, relax and enjoy.",
        "The series is complete, no more waiting for episodes!",
        "All episodes are ready, happy watching.",
        "Full series available, binge it all in one go!",
        "All episodes are here, wishing you a relaxing time.",
        "Enjoy the movie!",
        "Relax and enjoy this film.",
        "Popcorn ready? Let's start watching!",
        "A great movie awaits you. Enjoy!",
        "Take some time to relax with this movie."
    ],
    "ep_msg_completed_long": [
        "Don't binge the whole thing in one night, save your health for work!",
        "The series is full. Health first, don't stay up too late!",
        "The long journey is complete! Watch slowly to protect your eyes.",
        "It's a long series, remember to take breaks while binge-watching.",
        "This long series is complete, take your time to enjoy each episode.",
        "Full series out! Watch a little every day to fully enjoy it.",
        "A massive series has closed. Enjoy it slowly and happily.",
        "It's a long one, grab snacks and watch slowly!",
        "Don't pull an all-nighter, the series isn't going anywhere!",
        "Happy binge-watching, but remember to get enough sleep!"
    ],
    "ep_msg_past_missed": [
        "Episode {X} aired (delayed {DIFF} days).",
        "Episode {X} aired on TV but the app hasn't updated, be patient."
    ],
    "ep_msg_next_estimated": "Schedule for episode {X} is estimated on {DATE}.",
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
        
    # Remove old keys if they exist
    old_keys = ["ep_msg_completed_movie"]
    for k in old_keys:
        if k in data:
            del data[k]
            
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Updated {path}")

update_lang(vi_path, vi_keys)
update_lang(en_path, en_keys)

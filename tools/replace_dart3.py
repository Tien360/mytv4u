import re

def replace_in_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    for old, new in replacements:
        text = text.replace(old, new)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

replace_in_file('lib/screens/player_screen.dart', [
    ("'Tập '", "(L10n.t('ep_name') ?? 'Tập {name}').replaceAll('{name}', ep.name)"),
    ('"Tập "', "(L10n.t('ep_name') ?? 'Tập {name}').replaceAll('{name}', ep.name)"),
    ("'Từ đầu'", "L10n.t('from_beginning') ?? 'Từ đầu'"),
    ('"Từ đầu"', "L10n.t('from_beginning') ?? 'Từ đầu'"),
    ("'Xem tiếp'", "L10n.t('resume_playing') ?? 'Xem tiếp'"),
    ('"Xem tiếp"', "L10n.t('resume_playing') ?? 'Xem tiếp'"),
    ("'Bạn đã xem đến . Bạn muốn xem tiếp hay xem lại từ đầu?'", "(L10n.t('resume_prompt') ?? 'Bạn đã xem đến {time}. Bạn muốn xem tiếp hay xem lại từ đầu?').replaceAll('{time}', _formatDuration(Duration(milliseconds: savedPos)))"),
    ('"Không rõ"', "L10n.t('unknown') ?? 'Không rõ'"),
    ("'Không rõ'", "L10n.t('unknown') ?? 'Không rõ'"),
    ('"Tự động (Mặc định)"', "L10n.t('auto_default') ?? 'Tự động (Mặc định)'"),
    ("'Tự động (Mặc định)'", "L10n.t('auto_default') ?? 'Tự động (Mặc định)'"),
    ("'Luồng '", "(L10n.t('stream_id') ?? 'Luồng {id}').replaceAll('{id}', track.id)"),
    ('"Luồng "', "(L10n.t('stream_id') ?? 'Luồng {id}').replaceAll('{id}', track.id)"),
    ("'Tập tiếp theo sẽ phát sau  giây'", "(L10n.t('next_ep_in') ?? 'Tập tiếp theo sẽ phát sau {time} giây').replaceAll('{time}', remaining.toString())"),
    ("'Phim sẽ đóng sau  giây'", "(L10n.t('closing_in') ?? 'Phim sẽ đóng sau {time} giây').replaceAll('{time}', remaining.toString())"),
    ("'Kết thúc'", "L10n.t('finished') ?? 'Kết thúc'"),
    ('"Kết thúc"', "L10n.t('finished') ?? 'Kết thúc'"),
    ('"Đang chọn: "', "(L10n.t('selecting_track') ?? 'Đang chọn: {track}').replaceAll('{track}', _selectedAudioTrack != null ? _getTrackShortName(_selectedAudioTrack) : (L10n.t('auto_default') ?? 'Tự động'))"),
    ('"Đang chọn: "', "(L10n.t('selecting_track') ?? 'Đang chọn: {track}').replaceAll('{track}', _selectedSubtitleTrack != null ? _getTrackShortName(_selectedSubtitleTrack) : (L10n.t('auto_default') ?? 'Tự động'))"),
    ('"Đang chọn: "', "(L10n.t('selecting_track') ?? 'Đang chọn: {track}').replaceAll('{track}', _selectedSecondarySubtitleTrack != null ? _getTrackShortName(_selectedSecondarySubtitleTrack) : 'Tắt')"),
    ("'Tên phim'", "L10n.t('movie_title') ?? 'Tên phim'"),
    ("'Tập đang phát'", "L10n.t('current_ep') ?? 'Tập đang phát'"),
    ("'Thời lượng'", "L10n.t('duration') ?? 'Thời lượng'"),
    ("'Độ phân giải'", "L10n.t('resolution') ?? 'Độ phân giải'"),
    ("'Nguồn phát'", "L10n.t('streaming_source') ?? 'Nguồn phát'"),
    ("'Trình duyệt Web (Embed)'", "L10n.t('web_browser_embed') ?? 'Trình duyệt Web (Embed)'"),
    ("'Trình phát Video gốc'", "L10n.t('native_video_player') ?? 'Trình phát Video gốc'"),
    ("'Nguồn phụ: '", "(L10n.t('sub_source') ?? 'Nguồn phụ:') + ' '"),
    ("'Đang mở trình phát độ phân giải cao...\\n(Bấm ESC bên cửa sổ kia để thoát)'", "L10n.t('opening_high_res') ?? 'Đang mở trình phát độ phân giải cao...\\n(Bấm ESC bên cửa sổ kia để thoát)'"),
    ("'Quay lại'", "L10n.t('go_back') ?? 'Quay lại'"),
    ("'Tạm dừng (Space)'", "L10n.t('pause_space') ?? 'Tạm dừng (Space)'"),
    ("'Phát (Space)'", "L10n.t('play_space') ?? 'Phát (Space)'"),
    ("'Lùi 10s (←)'", "L10n.t('rewind_10s') ?? 'Lùi 10s (←)'"),
    ("'Tới 10s (→)'", "L10n.t('forward_10s') ?? 'Tới 10s (→)'"),
    ("'Âm lượng'", "L10n.t('volume') ?? 'Âm lượng'"),
    ("'Tập tiếp theo'", "L10n.t('next_episode') ?? 'Tập tiếp theo'"),
    ("'Danh sách tập'", "L10n.t('ep_list') ?? 'Danh sách tập'"),
    ("'Toàn màn hình'", "L10n.t('fullscreen') ?? 'Toàn màn hình'"),
    ("'Chọn tập'", "L10n.t('select_episode') ?? 'Chọn tập'")
])

print("Replaced in player_screen.dart")

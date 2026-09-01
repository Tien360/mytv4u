with open("lib/widgets/air_schedule_dialog.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("'Không tìm thấy ID TMDB'", "L10n.t('error_tmdb_id_not_found') ?? 'Không tìm thấy ID TMDB'")
c = c.replace("'Không có thông tin các Phần (Seasons).'", "L10n.t('error_no_seasons') ?? 'Không có thông tin các Phần (Seasons).'")
c = c.replace("'Phim chưa có phần nào hợp lệ.'", "L10n.t('error_no_valid_seasons') ?? 'Phim chưa có phần nào hợp lệ.'")
c = c.replace("'Lỗi: $e'", "L10n.t('error_prefix') != null ? '${L10n.t('error_prefix')}: $e' : 'Lỗi: $e'")
c = c.replace("'Lỗi tải tập phim: $e'", "L10n.t('error_loading_episodes') != null ? '${L10n.t('error_loading_episodes')}: $e' : 'Lỗi tải tập phim: $e'")
c = c.replace("'Phần ${s['season_number']}'", "${L10n.t('season') ?? 'Phần'} ${s['season_number']}")
c = c.replace("'Tập ${ep['episode_number']}'", "${L10n.t('episode') ?? 'Tập'} ${ep['episode_number']}")
c = c.replace("'Tập ${ep['episode_number']}: $name'", "${L10n.t('episode') ?? 'Tập'} ${ep['episode_number']}: $name")
c = c.replace("'Đã chiếu'", "L10n.t('released') ?? 'Đã chiếu'")
c = c.replace("'Sắp chiếu'", "L10n.t('upcoming') ?? 'Sắp chiếu'")
c = c.replace("'${ep['runtime']} phút'", "'${ep['runtime']} ${L10n.t('minutes') ?? 'phút'}'")
c = c.replace("'(${ep['vote_count'] ?? 0} votes)'", "'(${ep['vote_count'] ?? 0} ${L10n.t('votes') ?? 'đánh giá'})'")
c = c.replace("'Đạo diễn'", "L10n.t('director') ?? 'Đạo diễn'")
c = c.replace("'Biên kịch'", "L10n.t('writer') ?? 'Biên kịch'")
c = c.replace("'Diễn viên khách mời'", "L10n.t('guest_stars') ?? 'Diễn viên khách mời'")

with open("lib/widgets/air_schedule_dialog.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Updated L10n strings!")

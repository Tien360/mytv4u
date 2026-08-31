content = open('lib/screens/sport_screen.dart', 'r', encoding='utf-8').read()

content = content.replace('Tab(text: "Đang diễn ra (Live)")', 'Tab(text: L10n.t(''live-ongoing'') ?? "Đang diễn ra (Live)")')
content = content.replace('Tab(text: "Sắp diễn ra")', 'Tab(text: L10n.t(''live-upcoming'') ?? "Sắp diễn ra")')
content = content.replace('Tab(text: "Lịch Thi Đấu & Tỷ Số")', 'Tab(text: L10n.t(''live-schedule-scores'') ?? "Lịch Thi Đấu & Tỷ Số")')

content = content.replace("'Không có trận đấu nào đang diễn ra.'", "L10n.t(''no-live-matches'') ?? 'Không có trận đấu nào đang diễn ra.'")
content = content.replace("'Không có trận đấu nào sắp diễn ra.'", "L10n.t(''no-upcoming-matches'') ?? 'Không có trận đấu nào sắp diễn ra.'")

content = content.replace("match.league,", "match.league == 'Giải đấu khác' ? (L10n.t(''other-leagues'') ?? 'Giải đấu khác') : match.league,")

content = content.replace("'\ Nguồn phát'", "L10n.t(''sources-count'')?.replaceAll(''{count}'', match.sources.length.toString()) ?? '\ Nguồn phát'")
content = content.replace("'Chưa có nguồn'", "L10n.t(''no-sources-yet'') ?? 'Chưa có nguồn'")

content = content.replace("'Không có dữ liệu lịch thi đấu.'", "L10n.t(''no-schedule-data'') ?? 'Không có dữ liệu lịch thi đấu.'")

open('lib/screens/sport_screen.dart', 'w', encoding='utf-8').write(content)

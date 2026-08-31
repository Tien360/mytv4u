import json

paths = ['assets/langs/vi.json', 'assets/langs/en.json']

vi_add = {
  "open-link": "Mở Link",
  "open-file": "Mở File",
  "open-url-hint": "Nhập link video/audio/youtube (mp4, m3u8, youtube...)",
  "live-ongoing": "Đang diễn ra (Live)",
  "live-upcoming": "Sắp diễn ra",
  "live-schedule-scores": "Lịch Thi Đấu & Tỷ Số",
  "no-live-matches": "Không có trận đấu nào đang diễn ra.",
  "no-upcoming-matches": "Không có trận đấu nào sắp diễn ra.",
  "no-schedule-data": "Không có dữ liệu lịch thi đấu.",
  "other-leagues": "Giải đấu khác",
  "sources-count": "{count} Nguồn phát",
  "no-sources-yet": "Chưa có nguồn"
}

en_add = {
  "open-link": "Open Link",
  "open-file": "Open File",
  "open-url-hint": "Enter video/audio/youtube link (mp4, m3u8, youtube...)",
  "live-ongoing": "Live Now",
  "live-upcoming": "Upcoming",
  "live-schedule-scores": "Schedule & Scores",
  "no-live-matches": "No live matches available.",
  "no-upcoming-matches": "No upcoming matches available.",
  "no-schedule-data": "No schedule data available.",
  "other-leagues": "Other Leagues",
  "sources-count": "{count} Sources",
  "no-sources-yet": "No sources yet"
}

for p, add in zip(paths, [vi_add, en_add]):
    d = json.load(open(p, 'r', encoding='utf-8'))
    d.update(add)
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


import json

paths = ['assets/langs/vi.json', 'assets/langs/en.json']

vi_add = {
  "resume_watching": "Tiếp tục xem?",
  "resume_watching_desc": "Bạn đã xem đến {time}. Bạn muốn xem tiếp hay xem lại từ đầu?",
  "from_start": "Từ đầu",
  "resume_btn": "Tiếp tục",
  "next_ep_in": "Tập tiếp theo sẽ phát sau {time} giây",
  "close_in": "Phim sẽ đóng sau {time} giây"
}

en_add = {
  "resume_watching": "Resume playback?",
  "resume_watching_desc": "You left off at {time}. Would you like to resume or start over?",
  "from_start": "Start Over",
  "resume_btn": "Resume",
  "next_ep_in": "Next episode playing in {time}s",
  "close_in": "Closing in {time}s"
}

for p, add in zip(paths, [vi_add, en_add]):
    d = json.load(open(p, 'r', encoding='utf-8'))
    d.update(add)
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


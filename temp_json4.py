import json

def update_json(file_path, new_keys):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for k, v in new_keys.items():
        if k not in data:
            data[k] = v
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

vi_keys = {
  "rating_p": "Phim phổ biến đến mọi độ tuổi.",
  "rating_k": "Trẻ dưới 13 tuổi cần xem cùng người giám hộ.",
  "rating_t13": "Chỉ dành cho khán giả từ đủ 13 tuổi trở lên.",
  "rating_t16": "Chỉ dành cho khán giả từ đủ 16 tuổi trở lên.",
  "rating_t18": "Chỉ dành cho khán giả từ đủ 18 tuổi trở lên (Chứa nội dung nhạy cảm/bạo lực).",
  "rating_g": "Mọi lứa tuổi (Không chứa yếu tố nhạy cảm).",
  "rating_pg": "Trẻ em cần sự hướng dẫn của cha mẹ.",
  "rating_pg13": "Cảnh báo trẻ dưới 13 tuổi (Có bạo lực hoặc yếu tố nhạy cảm nhẹ).",
  "rating_r": "Dành cho người trưởng thành. Trẻ dưới 17 tuổi cần cha mẹ đi cùng.",
  "rating_nc17": "Nghiêm cấm trẻ em dưới 17 tuổi.",
  "rating_tv_y": "Mọi trẻ em.",
  "rating_tv_y7": "Trẻ em từ 7 tuổi trở lên.",
  "rating_tv_g": "Mọi lứa tuổi.",
  "rating_tv_pg": "Cần sự hướng dẫn của phụ huynh.",
  "rating_tv_14": "Dành cho người từ 14 tuổi trở lên.",
  "rating_tv_ma": "Chỉ dành cho khán giả trưởng thành (Chứa bạo lực, tình dục hoặc ngôn từ thô tục).",
  "rating_age_plus": "Dành cho khán giả từ {age} tuổi trở lên.",
  "rating_default": "Ký hiệu độ tuổi: {rating}"
}

en_keys = {
  "rating_p": "Suitable for all ages.",
  "rating_k": "Children under 13 must be accompanied by a guardian.",
  "rating_t13": "Restricted to viewers 13 years and older.",
  "rating_t16": "Restricted to viewers 16 years and older.",
  "rating_t18": "Restricted to adults 18+ (Contains sensitive/violent content).",
  "rating_g": "General Audiences. All ages admitted.",
  "rating_pg": "Parental Guidance Suggested. Some material may not be suitable for children.",
  "rating_pg13": "Parents Strongly Cautioned. Some material may be inappropriate for children under 13.",
  "rating_r": "Restricted. Under 17 requires accompanying parent or adult guardian.",
  "rating_nc17": "Adults Only. No one 17 and under admitted.",
  "rating_tv_y": "All children.",
  "rating_tv_y7": "Directed to older children (7+).",
  "rating_tv_g": "General audience.",
  "rating_tv_pg": "Parental guidance suggested.",
  "rating_tv_14": "Parents strongly cautioned. May be unsuitable for children under 14.",
  "rating_tv_ma": "Mature audiences only. May contain strong violence, sexual content, or coarse language.",
  "rating_age_plus": "Restricted to viewers {age} years and older.",
  "rating_default": "Age Rating: {rating}"
}

update_json("assets/langs/vi.json", vi_keys)
update_json("assets/langs/en.json", en_keys)
print("Updated JSON files")

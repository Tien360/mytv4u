import json
import os

def update_json(file_path, new_keys):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for k, v in new_keys.items():
        if k not in data:
            data[k] = v
            
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

en_keys = {
    "status": "Status",
    "budget": "Budget",
    "revenue": "Box Office",
    "production_companies": "Production Companies",
    "collection": "Collection",
    "recommendations": "More Like This",
    "director": "Director",
    "imdb_rating": "IMDb Rating",
    "searching_movie": "Searching for movie...",
    "movie_not_found": "Sorry, this movie is not yet available in our system."
}

vi_keys = {
    "status": "Trạng thái",
    "budget": "Kinh phí",
    "revenue": "Doanh thu",
    "production_companies": "Hãng sản xuất",
    "collection": "Bộ sưu tập",
    "recommendations": "Có thể bạn cũng thích",
    "director": "Đạo diễn",
    "imdb_rating": "Điểm IMDb",
    "searching_movie": "Đang tìm kiếm phim...",
    "movie_not_found": "Rất tiếc, hệ thống chưa cập nhật bộ phim này."
}

update_json("assets/langs/en.json", en_keys)
update_json("assets/langs/vi.json", vi_keys)
print("Updated localization files.")

import json, sys, urllib.request
sys.stdout.reconfigure(encoding="utf-8")

notes_vi = """🎮 Tích hợp Game mini YouTube Playables - chơi trực tiếp trong app.
🤖 Thêm tính năng Trợ lý tối ưu hóa.
📺 Cải thiện trải nghiệm trình cài đặt, TV, xem link YouTube.
🐛 Sửa lỗi nhỏ trình chơi phim."""

notes_en = """🎮 Integrated YouTube Playables mini games - play directly in the app.
🤖 Added Optimization Assistant feature.
📺 Improved installer, TV, and YouTube link viewing experience.
🐛 Fixed minor video player bugs."""

combined_notes = notes_vi + "\n\n---\n\n" + notes_en

version = "26.08.31.31.public"

body = {
    "fields": {
        "latest_version": {"stringValue": version},
        "download_url": {"stringValue": f"https://github.com/Tien360/mytv4u/releases/download/{version}/MyTV4U_Setup_{version}.exe"},
        "release_notes": {"stringValue": combined_notes},
    }
}

data = json.dumps(body).encode("utf-8")

for channel in ["public", "latest"]:
    url = f"https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/{channel}"
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json; charset=UTF-8"}, method="PATCH")
    try:
        with urllib.request.urlopen(req) as res:
            print(f"Updated {channel}: {res.status}")
    except Exception as e:
        print(f"Error {channel}: {e}")

print("Done!")

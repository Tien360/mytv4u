import json
import urllib.request

version = "26.08.22.k.beta"
notes = "🚀 Cập nhật Phiên bản 26.08.22.k.beta\n\n🎉 Tính năng mới:\n- Tự động nhận diện Livestream và ẩn thông báo Kết thúc phim ở màn hình Player."
channel = "beta"

url = f"https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/{channel}"

data = {
    "fields": {
        "latest_version": {"stringValue": version},
        "release_notes": {"stringValue": notes},
        "download_url": {"stringValue": f"https://github.com/Tien360/mytv4u/releases/download/{version}/MyTV4U_Setup_{version}.exe"},
        "is_force_update": {"booleanValue": True},
    }
}

req = urllib.request.Request(
    url, 
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json; charset=UTF-8'},
    method='PATCH'
)

try:
    with urllib.request.urlopen(req) as response:
        print("Success")
except urllib.error.URLError as e:
    print(f"Error: {e}")

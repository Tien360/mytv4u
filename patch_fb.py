import json
import urllib.request
from datetime import datetime, timezone

version = "26.08.22.j.beta"
notes = "🚀 Cập nhật Phiên bản 26.08.22.j.beta\n\n🎉 Tính năng mới:\n- Thêm chức năng mở URL/Link mạng trực tiếp\n- Sửa lỗi không hiển thị file âm thanh trong trình chọn file\n- Thiết kế lại icon riêng biệt cho các file mp3/wav khi đặt MyTV4U làm mặc định"
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
        print("Cập nhật Firebase thành công!")
except urllib.error.URLError as e:
    print(f"Lỗi Firebase: {e}")

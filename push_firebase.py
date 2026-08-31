import json
import urllib.request
import urllib.parse
import datetime

version = "26.08.31.20.public"
notes = "- Tối ưu UI Cài đặt: đồng bộ giao diện Ambient Background mượt mà.\n- Sửa lỗi cấu trúc UI của thẻ cài đặt Nhạc và Dropdown.\n- Bổ sung tuỳ chọn Bật/Tắt Giao diện Tối giản trong Cài đặt.\n- Cập nhật Trợ lý Tối ưu hoá gợi ý cho máy yếu/dùng pin."

url = "https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/public"
data = {
    "fields": {
      "latest_version": {"stringValue": version},
      "release_notes": {"stringValue": notes},
      "download_url": {"stringValue": f"https://github.com/Tien360/mytv4u/releases/download/{version}/MyTV4U_Setup_{version}.exe"},
      "is_force_update": {"booleanValue": False},
      "release_date": {"timestampValue": datetime.datetime.utcnow().isoformat() + "Z"}
    }
}
req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), method="PATCH")
req.add_header("Content-Type", "application/json; charset=UTF-8")

try:
    with urllib.request.urlopen(req) as response:
        print("Cập nhật Firebase thành công!")
except urllib.error.HTTPError as e:
    print(f"Lỗi: {e.code} {e.read().decode('utf-8')}")

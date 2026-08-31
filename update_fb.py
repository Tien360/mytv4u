import urllib.request
import json
import ssl

version = "26.08.25.11.public"
notes = "Chặn quảng cáo VMAP; Thiết kế gọn bảng Doanh thu neon; Thuật toán nhận diện chất lượng Premium siêu tốc và chi tiết trên từng tập; Sửa lỗi hiển thị đa ngôn ngữ."

url_public = "https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/public"
url_latest = "https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/latest"

body = {
    "fields": {
        "latest_version": {"stringValue": version},
        "download_url": {"stringValue": f"https://github.com/Tien360/mytv4u/releases/download/{version}/MyTV4U_Setup_{version}.exe"},
        "release_notes": {"stringValue": notes},
        "is_force_update": {"booleanValue": True}
    }
}
data = json.dumps(body).encode('utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req1 = urllib.request.Request(url_public, data=data, method='PATCH', headers={'Content-Type': 'application/json'})
urllib.request.urlopen(req1, context=ctx)

req2 = urllib.request.Request(url_latest, data=data, method='PATCH', headers={'Content-Type': 'application/json'})
urllib.request.urlopen(req2, context=ctx)

print("Firebase updated successfully")

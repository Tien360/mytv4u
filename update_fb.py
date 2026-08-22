import urllib.request
import json

version = "26.08.23.n.beta"
notes = "- Thêm chế độ Picture-in-Picture.\n- Tuỳ chọn Phát dưới nền."
channel = "beta"

url = f'https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/{channel}'
data = {
    "fields": {
        "latest_version": {"stringValue": version},
        "download_url": {"stringValue": f"https://github.com/Tien360/mytv4u/releases/download/{version}/MyTV4U_Setup_{version}.exe"},
        "release_notes": {"stringValue": notes},
        "is_mandatory": {"booleanValue": False}
    }
}
req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), method='PATCH')
req.add_header('Content-Type', 'application/json; charset=UTF-8')
try:
    with urllib.request.urlopen(req) as f:
        print(f"Firebase updated successfully! Status: {f.status}")
except urllib.error.HTTPError as e:
    print(f"Firebase error: {e.code} {e.read()}")

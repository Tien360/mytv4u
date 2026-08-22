
import urllib.request
import json

version = '26.08.19.k.beta'
channel = 'beta'
notes = '- Cập nhật: Sửa lỗi phân loại nhầm nguồn Film4K Archive vào tab Promax thay vì tab Standard.'

url = f'https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/{channel}'
data = {
    'fields': {
        'latest_version': {'stringValue': version},
        'download_url': {'stringValue': f'https://github.com/Tien360/mytv4u/releases/download/{version}/MyTV4U_Setup_{version}.exe'},
        'release_notes': {'stringValue': notes},
        'is_force_update': {'booleanValue': True}
    }
}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='PATCH')
try:
    with urllib.request.urlopen(req) as response:
        print('SUCCESS')
except Exception as e:
    print(e)


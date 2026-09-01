import urllib.request
import urllib.parse
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
prompt = "Tôi đang xem phim Class crush crisis, hãy tạo một bài thơ tiếng Việt 4 câu hài hước về phim này để trêu người xem. Chỉ in ra 4 câu thơ, không nói gì thêm."
url = "https://text.pollinations.ai/prompt/" + urllib.parse.quote(prompt)

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        print(response.read().decode('utf-8'))
except Exception as e:
    print("Error:", e)

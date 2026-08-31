import os

folder = r"C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.user_uploaded"
files = [
    "media_1787663029458.png",
    "media_1787663115534.png",
    "media_1787663220372.png"
]
for filename in files:
    path = os.path.join(folder, filename)
    with open(path, 'rb') as f:
        data = f.read(1024)
        print(f"{filename} starts with: {data[:8]}")
        is_apng = b'acTL' in data
        print(f"  APNG? {is_apng}")

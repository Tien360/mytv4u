with open("lib/screens/movie_detail_screen.dart", "rb") as f:
    content = f.read()

# Replace any BOM in the middle of the file
content = content.replace(b'\xef\xbb\xbf', b'')

with open("lib/screens/movie_detail_screen.dart", "wb") as f:
    f.write(content)
print("Removed BOM!")

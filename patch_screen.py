import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_call = """    final ytKey = await PhimApi.getTrailerStreamUrl(
      _movie!.name,
      _movie!.originalName,
      _movie!.year,
      isTv,
    );"""
    
new_call = """    final ytKey = await PhimApi.getTrailerStreamUrl(_movie!, isTv);"""

if old_call in content:
    content = content.replace(old_call, new_call)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated movie_detail_screen.dart")
else:
    print("Could not find old_call")

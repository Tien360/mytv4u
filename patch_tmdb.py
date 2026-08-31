import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\api\phim_api.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("append_to_response=recommendations,similar,credits", "append_to_response=recommendations,similar,credits,release_dates,content_ratings")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated TMDB API to fetch release_dates and content_ratings")

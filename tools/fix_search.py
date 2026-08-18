import json
import re

def add_keys(filepath, additions):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for k, v in additions.items():
        data[k] = v
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

add_keys('assets/langs/vi.json', {
    'search_tv': 'Tìm kiếm kênh TV...',
    'search_sports': 'Tìm kiếm sự kiện thể thao...',
    'search_movies': 'Tìm kiếm phim...'
})

add_keys('assets/langs/en.json', {
    'search_tv': 'Search TV channels...',
    'search_sports': 'Search sports events...',
    'search_movies': 'Search movies...'
})

with open('lib/screens/main_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("'Tìm kiếm kênh TV...'", "L10n.t('search_tv') ?? 'Tìm kiếm kênh TV...'")
text = text.replace("'Tìm kiếm sự kiện thể thao...'", "L10n.t('search_sports') ?? 'Tìm kiếm sự kiện thể thao...'")
text = text.replace("'Tìm kiếm phim...'", "L10n.t('search_movies') ?? 'Tìm kiếm phim...'")

with open('lib/screens/main_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Search placeholders localized")

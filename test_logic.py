import urllib.request
import json
import urllib.parse
import sys

sys.stdout.reconfigure(encoding='utf-8')
tmdb_api_key = "e9e9d8da18ae29fc430845952232787c"

def clean(t):
    import re
    t = re.sub(r'\(.*?\)', '', t)
    t = re.sub(r'\[.*?\]', '', t)
    t = re.sub(r'(?i)(vietsub|thuyết minh|lồng tiếng|bản đẹp|hd|fhd|4k|cam|ts|bluray|web-dl|tập \d+)', '', t)
    return t.strip()

def search_tmdb(title, orig, year, is_tv):
    c_orig = clean(orig)
    c_title = clean(title)
    
    queries = []
    if c_orig: queries.append(c_orig)
    if c_title and c_title not in queries: queries.append(c_title)
    if orig and orig not in queries: queries.append(orig)
    if title and title not in queries: queries.append(title)
    
    for q in queries:
        url = f"https://api.themoviedb.org/3/search/multi?query={urllib.parse.quote(q)}&api_key={tmdb_api_key}&language=vi-VN"
        try:
            res = urllib.request.urlopen(url).read().decode('utf-8')
            data = json.loads(res)
            if data['results']:
                for m in data['results']:
                    if year:
                        y = m.get('release_date', m.get('first_air_date', ''))
                        if y.startswith(year):
                            return m
                return data['results'][0]
        except Exception as e:
            print("Error", e)
    return None

def get_trailer(title, orig, year, is_tv):
    match = search_tmdb(title, orig, year, is_tv)
    if match:
        print("TMDB Match:", match.get('title', match.get('name')), "ID:", match['id'], "Type:", match.get('media_type'))
        v_url = f"https://api.themoviedb.org/3/{match.get('media_type', 'movie')}/{match['id']}/videos?api_key={tmdb_api_key}"
        try:
            v_res = urllib.request.urlopen(v_url).read().decode('utf-8')
            v_data = json.loads(v_res)
            for v in v_data.get('results', []):
                print("  Video:", v['key'], v['type'], v['name'])
        except Exception as e:
            print("  Video Error:", e)
    else:
        print("No TMDB match")

print("--- Sư Huynh ---")
get_trailer("Sư Huynh Quá Cẩn Trọng", "Pull Strings", "2026", True)

print("--- Đặc vụ kim sao thế ---")
get_trailer("Đặc vụ kim sao thế", "Đặc vụ kim sao thế", "", True)
get_trailer("Thư ký kim sao thế", "What's Wrong with Secretary Kim", "", True)

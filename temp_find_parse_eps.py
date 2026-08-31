import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/api/phim_api.dart', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("List<EpisodeServer> _parseEpisodes")
if idx != -1:
    print(content[idx:idx+2500])

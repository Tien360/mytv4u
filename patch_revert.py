import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

bad_block = """      if (bestMeta == null) {
         String res = '';
         if (maxScore == 4) res = '4K';
         else if (maxScore == 3) res = '1080p';
         else if (maxScore == 2) res = '720p';
         
         if (res.isNotEmpty) {
           bestMeta = {'resolution': res, 'hdr': 'Unknown', 'audioTracks': []};
           final firstEp = premiumEps.firstWhere((e) => e['score'] == maxScore, orElse: () => premiumEps.first);
           bestMeta!['fallback_filename'] = firstEp['filename'];
         }
      }"""
content = content.replace(bad_block, "")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)

print("Reverted fallback logic")

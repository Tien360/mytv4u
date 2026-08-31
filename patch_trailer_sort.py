import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\api\phim_api.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_block = """          if (videoData['results'] != null && videoData['results'].isNotEmpty) {
            final List results = videoData['results'];
            var trailer = results.firstWhere(
              (v) => v['site'] == 'YouTube' && v['type'] == 'Trailer',
              orElse: () => null,
            );
            trailer ??= results.firstWhere(
              (v) => v['site'] == 'YouTube',
              orElse: () => null,
            );

            if (trailer != null) {
              return trailer['key'];
            }
          }"""

new_block = """          if (videoData['results'] != null && videoData['results'].isNotEmpty) {
            final List results = videoData['results'];
            List<String> langs = ['vi', 'en', 'ko', 'zh', 'ja', 'th', 'es', 'fr', 'de', 'ru', 'pt', 'it', 'hi', 'tl', 'id', 'ms', 'ar', 'tr', ''];
            
            for (var lang in langs) {
              var trailer = results.firstWhere(
                (v) => v['site'] == 'YouTube' && v['type'] == 'Trailer' && (v['iso_639_1'] == lang || (lang == '' && v['iso_639_1'] == null)),
                orElse: () => null,
              );
              if (trailer != null) return trailer['key'];
            }
            
            for (var lang in langs) {
              var trailer = results.firstWhere(
                (v) => v['site'] == 'YouTube' && (v['iso_639_1'] == lang || (lang == '' && v['iso_639_1'] == null)),
                orElse: () => null,
              );
              if (trailer != null) return trailer['key'];
            }

            var trailer = results.firstWhere(
              (v) => v['site'] == 'YouTube',
              orElse: () => null,
            );
            if (trailer != null) {
              return trailer['key'];
            }
          }"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated trailer parsing block")
else:
    print("Old block not found")

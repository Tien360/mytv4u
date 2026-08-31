import re

with open('lib/api/tv_api.dart', 'r', encoding='utf-8') as f:
    content = f.read()

old_func_body = '''            String streamUrl = '';
            for (int j = i + 1; j < lines.length; j++) {
              if (lines[j].trim().startsWith('#EXT')) continue;
              if (lines[j].trim().isNotEmpty) {
                streamUrl = lines[j].trim();
                break;
              }
            }
            
            if (streamUrl.isNotEmpty && !streamUrl.contains('youtube.com')) {'''

new_func_body = '''            String streamUrl = '';
            String drmKid = '';
            String drmKey = '';
            
            for (int j = i + 1; j < lines.length; j++) {
              String l = lines[j].trim();
              if (l.isEmpty) continue;
              
              if (l.startsWith('#KODIPROP:inputstream.adaptive.license_key=')) {
                String keyStr = l.replaceAll('#KODIPROP:inputstream.adaptive.license_key=', '').trim();
                // format can be kid:key or just key, usually kid:key
                final keyParts = keyStr.split(':');
                if (keyParts.length == 2) {
                  drmKid = keyParts[0];
                  drmKey = keyParts[1];
                }
                continue;
              }
              
              if (l.startsWith('#')) {
                continue; // Skip all other # tags like #EXT, #KODIPROP etc
              }
              
              streamUrl = l;
              break;
            }
            
            if (streamUrl.isNotEmpty && !streamUrl.contains('youtube.com')) {
              if (drmKid.isNotEmpty && drmKey.isNotEmpty) {
                streamUrl = streamUrl + '|drm:{"' + drmKid + '":"' + drmKey + '"}';
              }'''

content = content.replace(old_func_body, new_func_body)

with open('lib/api/tv_api.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched tv_api.dart with DRM support successfully!")

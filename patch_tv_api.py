import re

with open('lib/api/tv_api.dart', 'r', encoding='utf-8') as f:
    content = f.read()

old_func = '''  static Future<List<TvChannel>> getChannels() async {
    List<TvChannel> channels = List.from(defaultChannels);
    try {
      final response = await http.get(Uri.parse('https://tinhlagi.pro/tivi/'));'''

new_func = '''  static Future<List<TvChannel>> getChannels() async {
    List<TvChannel> channels = [];
    
    try {
      final res = await http.get(Uri.parse('https://raw.githubusercontent.com/vuminhthanh12/vuminhthanh12/refs/heads/main/vmttv'));
      if (res.statusCode == 200) {
        final lines = res.body.split('\\n');
        for (int i = 0; i < lines.length; i++) {
          final line = lines[i].trim();
          if (line.startsWith('#EXTINF:')) {
            String logo = '';
            String group = 'Khác';
            
            final logoMatch = RegExp(r'tvg-logo="([^"]+)"').firstMatch(line);
            if (logoMatch != null) logo = logoMatch.group(1)!;
            
            final groupMatch = RegExp(r'group-title="([^"]+)"').firstMatch(line);
            if (groupMatch != null) group = groupMatch.group(1)!;
            
            final parts = line.split(',');
            String name = parts.length > 1 ? parts.last.trim() : 'Unknown';
            
            String streamUrl = '';
            for (int j = i + 1; j < lines.length; j++) {
              if (lines[j].trim().startsWith('#EXT')) continue;
              if (lines[j].trim().isNotEmpty) {
                streamUrl = lines[j].trim();
                break;
              }
            }
            
            if (streamUrl.isNotEmpty && !streamUrl.contains('youtube.com')) {
              channels.add(TvChannel(
                id: 'vmttv_' + i.toString(),
                name: name,
                category: group,
                logo: logo,
                streamUrl: streamUrl,
              ));
            }
          }
        }
      }
    } catch (e) {
      print('Error parsing vmttv: \');
    }

    try {
      final response = await http.get(Uri.parse('https://tinhlagi.pro/tivi/'));'''

content = content.replace(old_func, new_func)

old_end = '''    } catch (e) {
      print('Error loading HTML TV Channels: \');
    }

    return channels;
  }'''

new_end = '''    } catch (e) {
      print('Error loading HTML TV Channels: \');
    }

    for (var defC in defaultChannels) {
      if (!channels.any((c) => c.name == defC.name || (c.streamUrl.isNotEmpty && c.streamUrl == defC.streamUrl))) {
        channels.add(defC);
      }
    }

    return channels;
  }'''

content = content.replace(old_end, new_end)

with open('lib/api/tv_api.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched tv_api.dart successfully!")

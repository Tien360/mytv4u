import re

with open('lib/api/tv_api.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the start and end of the getChannels function
start_idx = content.find('  static Future<List<TvChannel>> getChannels() async {')
end_idx = content.find('  }', start_idx) + 3

if start_idx != -1 and end_idx != -1:
    old_func = content[start_idx:end_idx]
    
    new_func = '''  static Future<List<TvChannel>> getChannels() async {
    List<TvChannel> channels = List.from(defaultChannels);
    try {
      final response = await http.get(Uri.parse('https://tinhlagi.pro/tivi/'));
      if (response.statusCode == 200) {
        final document = html_parser.parse(response.body);
        final headings = document.querySelectorAll('h2.group-title');
        
        for (var heading in headings) {
          String category = heading.text.trim();
          category = category.replaceAll(RegExp(r'\\s*\\(\\d+\\)$'), '').trim();
          
          final grid = heading.nextElementSibling;
          if (grid != null && grid.classes.contains('channel-grid')) {
            final aTags = grid.querySelectorAll('a.channel-card');
            
            for (var a in aTags) {
              final href = a.attributes['href'] ?? '';
              final uri = Uri.parse('https://tinhlagi.pro/tivi/' + href);
              String streamUrl = uri.queryParameters['url'] ?? '';
              final name = uri.queryParameters['name'] ?? a.querySelector('.channel-name')?.text.trim() ?? 'Unknown';
              final logo = a.querySelector('img')?.attributes['src'] ?? '';
              
              if (streamUrl.contains('youtube.com') || streamUrl.contains('youtu.be')) continue;
              
              // Map Category
              String mappedCategory = category;
              
              String webUrl = '';
              if (streamUrl.isEmpty) {
                if (name.toLowerCase().contains('thvl')) {
                  webUrl = 'https://www.thvli.vn/live/thvl1-hd';
                  streamUrl = '';
                }
              }
              
              if ((streamUrl.isNotEmpty || webUrl.isNotEmpty)) {
                int existingIdx = channels.indexWhere((c) => (streamUrl.isNotEmpty && c.streamUrl == streamUrl) || c.name == name);
                if (existingIdx != -1) {
                  if (channels[existingIdx].logo.isEmpty && logo.isNotEmpty) {
                    channels[existingIdx] = channels[existingIdx].copyWith(logo: logo);
                  }
                } else {
                  channels.add(TvChannel(
                    id: 'tl_\',
                    name: name,
                    category: mappedCategory,
                    logo: logo,
                    streamUrl: streamUrl,
                    webUrl: webUrl,
                  ));
                }
              }
            }
          }
        }
      }
    } catch (e) {
      print('Error loading HTML TV Channels: \');
    }

    return channels;
  }'''
    
    content = content.replace(old_func, new_func)
    
    with open('lib/api/tv_api.dart', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Reverted tv_api.dart successfully!")
else:
    print("Could not find getChannels function.")

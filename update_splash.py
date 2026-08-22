import re

with open('lib/screens/splash_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports
if "import '../models/movie.dart';" not in content:
    content = "import '../models/movie.dart';\n" + content
if "import 'player_screen.dart';" not in content:
    content = "import 'player_screen.dart';\n" + content
if "import 'dart:io';" not in content:
    content = "import 'dart:io';\n" + content

# Replace logic
old_logic = r"""    if (deepLink != null &&
        deepLink.action == 'movie' &&
        deepLink.slug.isNotEmpty) {
      Future.delayed(const Duration(milliseconds: 500), () {
        DeepLinkService.navigatorKey.currentState?.push(
          MaterialPageRoute(
            builder: (_) => MovieDetailScreen(slug: deepLink.slug),
          ),
        );
      });
    }"""

new_logic = r"""    if (deepLink != null) {
      Future.delayed(const Duration(milliseconds: 500), () {
        if (deepLink.action == 'movie' && deepLink.slug.isNotEmpty) {
          DeepLinkService.navigatorKey.currentState?.push(
            MaterialPageRoute(
              builder: (_) => MovieDetailScreen(slug: deepLink.slug),
            ),
          );
        } else if (deepLink.action == 'local_file' && deepLink.slug.isNotEmpty) {
          final file = File(deepLink.slug);
          if (file.existsSync()) {
            final filename = deepLink.slug.split('\\').last.split('/').last;
            final fileUrl = 'file:///' + deepLink.slug.replaceAll('\\', '/');
            DeepLinkService.navigatorKey.currentState?.push(
              MaterialPageRoute(
                builder: (_) => PlayerScreen(
                  episodes: [
                    Episode(
                      name: 'Full',
                      slug: 'full',
                      m3u8Url: fileUrl,
                      embedUrl: '',
                    )
                  ],
                  currentEpisodeIndex: 0,
                  movieName: filename,
                ),
              ),
            );
          }
        }
      });
    }"""

# Use regex to find old logic ignoring whitespace
content = re.sub(r'    if \(deepLink \!= null &&.*?\}\);?\s*\}', new_logic, content, flags=re.DOTALL)

with open('lib/screens/splash_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated splash_screen.dart")

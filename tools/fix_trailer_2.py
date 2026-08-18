import re

with open('lib/screens/movie_detail_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the HTML script
html_pattern = r'(var player;\s*)(function onYouTubeIframeAPIReady\(\) \{)'
replacement = r'''\1window.dartShouldPause = false;
        setInterval(function() {
          if (window.dartShouldPause && typeof player !== 'undefined' && player && player.pauseVideo) {
            player.pauseVideo();
            window.dartShouldPause = false;
          }
        }, 500);
        \2'''
text = re.sub(html_pattern, replacement, text)

with open('lib/screens/movie_detail_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated HTML logic")

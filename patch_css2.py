import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\youtube_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern_inject = r"var style = document\.createElement\('style'\);[\s\S]*?document\.head\.appendChild\(style\);"
repl_inject = """if (!document.getElementById('yt-tweak-style')) {
          var style = document.createElement('style');
          style.id = 'yt-tweak-style';
          style.innerHTML = `
            ytd-ad-slot-renderer, ytd-banner-promo-renderer, ytd-player-legacy-desktop-watch-ads-renderer,
            ytd-action-companion-ad-renderer, .ytd-in-feed-ad-layout-renderer, #masthead-ad {
              display: none !important;
            }
            html, body, ytd-app, ytd-page-manager, #background, #page-manager, 
            ytd-browse, ytd-two-column-browse-results-renderer, ytd-rich-grid-renderer {
              background: transparent !important;
              background-color: transparent !important;
            }
            html[dark], html {
              --yt-spec-base-background: transparent !important;
              --yt-spec-brand-background-solid: transparent !important;
              --yt-spec-brand-background-primary: transparent !important;
              --yt-spec-general-background-a: transparent !important;
              --yt-spec-general-background-b: transparent !important;
              --yt-spec-general-background-c: transparent !important;
              --yt-spec-menu-background: rgba(30,30,30,0.8) !important;
            }
          `;
          document.documentElement.appendChild(style);
        }
        
        // Use MutationObserver to aggressively remove backgrounds from any injected #background element
        if (!window.ytBgObserver) {
          window.ytBgObserver = new MutationObserver((mutations) => {
            var bg = document.querySelector('#background');
            if (bg) bg.style.setProperty('background', 'transparent', 'important');
            var app = document.querySelector('ytd-app');
            if (app) app.style.setProperty('background', 'transparent', 'important');
          });
          window.ytBgObserver.observe(document.documentElement, { childList: true, subtree: true });
        }"""
content = re.sub(pattern_inject, repl_inject, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated CSS in youtube_screen.dart")

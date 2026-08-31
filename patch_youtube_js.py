import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\youtube_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace _injectYoutubeTweaks to hook pushState and replaceState
pattern_inject = r"String js = '''[\s\S]*?''';"
repl_inject = """String js = '''
      // Force Dark Mode
      document.documentElement.setAttribute('dark', 'true');
      
      // Hide Ads and remove background
      var style = document.createElement('style');
      style.innerHTML = `
        ytd-ad-slot-renderer, ytd-banner-promo-renderer, ytd-player-legacy-desktop-watch-ads-renderer,
        ytd-action-companion-ad-renderer, .ytd-in-feed-ad-layout-renderer, #masthead-ad {
          display: none !important;
        }
        html, body, ytd-app, #background.ytd-app, ytd-page-manager {
          background: transparent !important;
          background-color: transparent !important;
        }
      `;
      document.head.appendChild(style);

      // Hook SPA navigation (yt-navigate)
      if (!window.hasInjectedYtHook) {
        window.hasInjectedYtHook = true;
        const originalPushState = history.pushState;
        const originalReplaceState = history.replaceState;
        
        function checkUrlAndStop(url) {
          if (url.includes('/watch') || url.includes('/shorts/') || url.includes('/live/') || url.includes('/playlist?list=')) {
            // Stop video if it started
            var vids = document.querySelectorAll('video');
            for(var i=0; i<vids.length; i++) vids[i].pause();
            
            window.chrome.webview.postMessage({ "url": url });
            history.back(); // Immediately go back to browsing
          }
        }

        history.pushState = function() {
          originalPushState.apply(this, arguments);
          checkUrlAndStop(location.href);
        };
        history.replaceState = function() {
          originalReplaceState.apply(this, arguments);
          checkUrlAndStop(location.href);
        };
        window.addEventListener('popstate', function() {
          checkUrlAndStop(location.href);
        });
        
        // Also catch standard clicks just in case
        document.addEventListener('click', function(e) {
          var a = e.target.closest('a');
          if (a && a.href) {
            if (a.href.includes('/watch') || a.href.includes('/shorts/') || a.href.includes('/live/') || a.href.includes('/playlist?list=')) {
              e.preventDefault();
              e.stopPropagation();
              checkUrlAndStop(a.href);
            }
          }
        }, true);
      }
    ''';"""
content = re.sub(pattern_inject, repl_inject, content)

# Fix _handleYoutubeLink to correctly pass the URL to m3u8Url
pattern_handle = r"void _handleYoutubeLink\(String url\) \{[\s\S]*?if \(vid != null\) \{"
repl_handle = """void _handleYoutubeLink(String url) {
    String? vid;
    if (url.contains('/watch')) {
      final uri = Uri.parse(url);
      vid = uri.queryParameters['v'] ?? uri.queryParameters['list'];
    } else if (url.contains('/shorts/')) {
      vid = url.split('/shorts/').last.split('?').first;
    } else if (url.contains('/live/')) {
      vid = url.split('/live/').last.split('?').first;
    } else if (url.contains('/playlist?list=')) {
      final uri = Uri.parse(url);
      vid = uri.queryParameters['list'];
    }

    if (vid != null || url.isNotEmpty) {"""
content = re.sub(pattern_handle, repl_handle, content)

pattern_ep = r"filename: vid,[\s]*m3u8Url: '',[\s]*embedUrl: '',"
repl_ep = "filename: vid ?? 'yt_video',\n        m3u8Url: url,\n        embedUrl: '',"
content = re.sub(pattern_ep, repl_ep, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated youtube_screen js intercept and m3u8Url")

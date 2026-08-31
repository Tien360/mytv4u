import 'package:flutter/material.dart';
import 'package:webview_windows/webview_windows.dart';
import 'package:flutter/services.dart';
import 'dart:convert';
import '../models/movie.dart';
import 'player_screen.dart';

class YoutubeScreen extends StatefulWidget {
  const YoutubeScreen({Key? key}) : super(key: key);

  @override
  State<YoutubeScreen> createState() => YoutubeScreenState();
}

class YoutubeScreenState extends State<YoutubeScreen> {
  final _controller = WebviewController();
  bool _isWebviewInitialized = false;

  @override
  void initState() {
    super.initState();
    initWebview();
  }

  Future<void> initWebview() async {
    try {
      await _controller.initialize();
      await _controller.setBackgroundColor(Colors.transparent);
      _controller.url.listen((url) {
        if (url.contains('/watch') || url.contains('/shorts/') || url.contains('/live/') || url.contains('/playlist?list=')) {
          _controller.goBack();
          _handleYoutubeLink(url);
        }
      });

      _controller.webMessage.listen((message) {
        if (message.containsKey('url')) {
          _handleYoutubeLink(message['url']);
        }
      });

      await _controller.loadUrl('https://www.youtube.com');
      if (mounted) {
        setState(() {
          _isWebviewInitialized = true;
        });
      }

      // Inject JS to block ads and intercept clicks
      // Note: we do this when page starts loading or finishes.
      // webview_windows doesn't have onLoadStop easily, but we can poll or use HistoryChanged.
      _controller.historyChanged.listen((event) async {
        await _injectYoutubeTweaks();
      });

    } catch (e) {
      debugPrint("Webview init error: $e");
    }
  }

  Future<void> _injectYoutubeTweaks() async {
    if (!_isWebviewInitialized) return;
    
    // Force dark mode, block ads, and intercept video clicks
    String js = '''
      // Force Dark Mode
      document.documentElement.setAttribute('dark', 'true');
      
      // Hide Ads and remove background
      if (!document.getElementById('yt-tweak-style')) {
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
        }

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
    ''';
    try {
      await _controller.executeScript(js);
    } catch(e) {}
  }

  void _handleYoutubeLink(String url) {
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

    if (vid != null || url.isNotEmpty) {
      // Create a dummy movie and episode
      

      final ep = Episode(
        name: 'Full',
        slug: 'full',
        filename: vid ?? 'yt_video',
        m3u8Url: url,
        embedUrl: '',
      );

      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => PlayerScreen(
            episodes: [ep],
            movieName: 'YouTube Video',
            currentEpisodeIndex: 0,
            lazyPlaylistUrl: url,
          ),
        ),
      );
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (!_isWebviewInitialized) {
      return const Center(child: CircularProgressIndicator());
    }
    return Stack(
      children: [
        Webview(_controller),
      ],
    );
  }
}

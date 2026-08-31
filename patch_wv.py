import re

def patch_webview_autoplay(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    js_inject = "              } catch(e) {}\\n              \\n              setTimeout(() => {\\n                try {\\n                  var video = document.querySelector('video');\\n                  if (video) {\\n                    video.muted = false; \\n                    video.play().catch(e => {\\n                        video.muted = true;\\n                        video.play();\\n                    });\\n                  }\\n                } catch(e) {}\\n              }, 1000);\\n            ''');"
            
    content = content.replace("              } catch(e) {}\\n            ''');", js_inject)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_webview_autoplay('lib/screens/tv_webview_screen.dart')
print("Patched tv_webview_screen.dart")

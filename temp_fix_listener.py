import sys
with open('lib/screens/game_player_screen.dart', 'r', encoding='utf-8') as f:
    c = f.read()

target = """      _controller.historyChanged.listen((event) async {
        if (event.url != null && event.url!.contains("playables")) {
           await _injectFullscreenScript();
        }
      });"""
new_target = """      _controller.url.listen((url) async {
        if (url.contains("playables")) {
           await _injectFullscreenScript();
        }
      });"""

if target in c:
    c = c.replace(target, new_target)
    print("Fixed url listener")
else:
    print("Could not find target")

with open('lib/screens/game_player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(c)

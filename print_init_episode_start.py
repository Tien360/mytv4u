import sys
sys.stdout.reconfigure(encoding='utf-8')
with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

start_idx = text.find("Future<void> _initEpisode(int index) async {")
print(text[start_idx:start_idx+2000])

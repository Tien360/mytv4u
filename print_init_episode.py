import sys
sys.stdout.reconfigure(encoding='utf-8')
with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

start_idx = text.find("Future<void> _initEpisode(int index) async {")
end_idx = text.find("void _playNextEpisode() {")
print(text[start_idx:end_idx])

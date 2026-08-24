with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

start_idx = text.find("void _saveLocalProgress() async {")
if start_idx != -1:
    print(text[start_idx:start_idx+400])
else:
    print("Not found")

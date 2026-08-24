with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

start_idx = text.find("if (savedPos > 5000 && mounted && ep.slug != 'trailer') {")
if start_idx != -1:
    print(text[start_idx-100:start_idx+100])
else:
    print("Not found")

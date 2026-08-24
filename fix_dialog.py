with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

old_cond = "if (savedPos > 5000 && mounted && ep.slug != 'trailer') {"
new_cond = "if (savedPos > 5000 && mounted && ep.slug != 'trailer' && !widget.isLive) {"

if old_cond in text:
    text = text.replace(old_cond, new_cond)
    with open("lib/screens/player_screen.dart", "w", encoding="utf-8") as f:
        f.write(text)
    print("Fixed continue watching dialog for live streams.")
else:
    print("Condition not found.")

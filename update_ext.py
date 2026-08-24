with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("'assets/easter/dynamite.jpg'", "'assets/easter/dynamite.png'")
text = text.replace("'assets/easter/tissue.jpg'", "'assets/easter/tissue.png'")
text = text.replace("'assets/easter/teddy.jpg'", "'assets/easter/teddy.png'")
text = text.replace("'assets/easter/ufo.jpg'", "'assets/easter/ufo.png'")

with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated image extensions to .png for transparency!")

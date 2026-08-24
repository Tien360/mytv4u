with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Action
text = text.replace("'assets/lottie/noto_1f4a5.json',", "'assets/easter/dynamite.jpg', 'assets/lottie/noto_1f4a5.json',")
# Rage
text = text.replace("'assets/lottie/noto_1f92c.json',", "'assets/easter/dynamite.jpg', 'assets/lottie/noto_1f92c.json',")

# Romance
text = text.replace("'assets/lottie/noto_1f496.json',", "'assets/easter/teddy.jpg', 'assets/lottie/noto_1f496.json',")

# Scifi
text = text.replace("'assets/lottie/noto_1f680.json',", "'assets/easter/ufo.jpg', 'assets/lottie/noto_1f680.json',")

# Cry
text = text.replace("'assets/lottie/noto_1f62d.json',", "'assets/easter/tissue.jpg', 'assets/lottie/noto_1f62d.json',")

# Comedy (let's add tissue to comedy too for tears of joy)
text = text.replace("'assets/lottie/noto_1f602.json',", "'assets/easter/tissue.jpg', 'assets/lottie/noto_1f602.json',")


with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(text)

print("Injected new AI image stickers into pools!")

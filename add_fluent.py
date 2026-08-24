import urllib.request
import os

urls = {
    'fluent_alien.png': "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Alien/3D/alien_3d.png",
    'fluent_ghost.png': "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Ghost/3D/ghost_3d.png",
    'fluent_skull.png': "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Skull/3D/skull_3d.png",
    'fluent_clown.png': "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Clown%20face/3D/clown_face_3d.png",
    'fluent_popcorn.png': "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Popcorn/3D/popcorn_3d.png",
    'fluent_party.png': "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Partying%20face/3D/partying_face_3d.png",
    'fluent_crying.png': "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Loudly%20crying%20face/3D/loudly_crying_face_3d.png",
    'fluent_angry.png': "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Pouting%20face/3D/pouting_face_3d.png",
    'fluent_heart.png': "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Sparkling%20heart/3D/sparkling_heart_3d.png"
}

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

for name, url in urls.items():
    try:
        urllib.request.urlretrieve(url, f"assets/easter/{name}")
        print(f"Downloaded {name}")
    except Exception as e:
        print(f"Failed {name}: {e}")

# Inject into dart file
with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("'assets/easter/ufo.png'", "'assets/easter/fluent_alien.png', 'assets/easter/ufo.png'")
text = text.replace("'assets/lottie/noto_1f47b.json'", "'assets/easter/fluent_ghost.png', 'assets/easter/fluent_skull.png', 'assets/lottie/noto_1f47b.json'")
text = text.replace("'assets/easter/tissue.png'", "'assets/easter/fluent_clown.png', 'assets/easter/tissue.png'")
text = text.replace("'assets/easter/popcorn.jpg'", "'assets/easter/fluent_popcorn.png', 'assets/easter/popcorn.jpg'")
text = text.replace("'assets/lottie/noto_1f389.json'", "'assets/easter/fluent_party.png', 'assets/lottie/noto_1f389.json'")
text = text.replace("'assets/lottie/noto_1f62d.json'", "'assets/easter/fluent_crying.png', 'assets/lottie/noto_1f62d.json'")
text = text.replace("'assets/lottie/noto_1f92c.json'", "'assets/easter/fluent_angry.png', 'assets/lottie/noto_1f92c.json'")
text = text.replace("'assets/easter/teddy.png'", "'assets/easter/fluent_heart.png', 'assets/easter/teddy.png'")

with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(text)

print("Injected Fluent 3D Emojis!")

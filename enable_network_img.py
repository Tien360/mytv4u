with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    text = f.read()

old_code = """      } else if (url.endsWith('.jpg') || url.endsWith('.png')) {
        contentWidget = Image.asset(url)
            .animate(onPlay: (c) => c.repeat(reverse: true))
            .scale(begin: const Offset(1,1), end: const Offset(1.1, 1.1), duration: 600.ms)
            .rotate(begin: -0.05, end: 0.05, duration: 600.ms);"""

new_code = """      } else if (url.endsWith('.jpg') || url.endsWith('.png') || url.endsWith('.webp')) {
        contentWidget = (url.startsWith('http') ? Image.network(url) : Image.asset(url))
            .animate(onPlay: (c) => c.repeat(reverse: true))
            .scale(begin: const Offset(1,1), end: const Offset(1.1, 1.1), duration: 600.ms)
            .rotate(begin: -0.05, end: 0.05, duration: 600.ms);"""

text = text.replace(old_code, new_code)

with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(text)

print("Enabled Image.network for jpg/png/webp")

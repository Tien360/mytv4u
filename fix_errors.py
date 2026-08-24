with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Fix movie id -> slug
text = text.replace("widget.movie?.id", "widget.movie?.slug")

# Fix bounce
text = text.replace("textWidget.animate().bounce()", "textWidget.animate().scale().moveY(end: -5, duration: 200.ms)")

# Fix emoji bed
text = text.replace("🛏️", "")
text = text.replace("⏳", "")

with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Fixed widget")

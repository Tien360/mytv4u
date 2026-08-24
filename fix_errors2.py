with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("oldWidget.movie?.id", "oldWidget.movie?.slug")

# Fix string
text = text.replace('Time to sleep! Do not binge watch all night', "Time to sleep! Do not binge watch all night")

with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Fixes applied")

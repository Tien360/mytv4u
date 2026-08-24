with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    text = f.read()

# I will just replace the specific broken lines
text = text.replace("'Time to sleep! Don\\'t binge watch all night'", '"Time to sleep! Do not binge watch all night"')
text = text.replace("'Time to sleep! Don't binge watch all night'", '"Time to sleep! Do not binge watch all night"')

with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Fixed quote")

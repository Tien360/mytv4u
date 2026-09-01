with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("?? (L10n.t('this_movie') ?? 'This movie');", "?? L10n.t('this_movie');")

with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Removed dead code")

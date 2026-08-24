with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Fix order of seasonNum
text = text.replace("int seasonNum = nextEpMap['season_number'] ?? 1;", "")
text = text.replace("String nextInfo = '';", "int seasonNum = nextEpMap['season_number'] ?? 1;\n        String nextInfo = '';")

# Fix SnackBar quote
text = text.replace("'Time to sleep! Don't binge watch all night '", '"Time to sleep! Don\'t binge watch all night "')

with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Fixes applied properly")

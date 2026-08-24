import re

with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Replace {X} formatting
old_replace = "_msg = _msg.replaceAll('{X}', nextEpNum.toString());"
new_replace = """int seasonNum = nextEpMap['season_number'] ?? 1;
        String displayX = seasonNum > 1 ? '$nextEpNum (Mùa $seasonNum)' : nextEpNum.toString();
        _msg = _msg.replaceAll('{X}', displayX);"""
text = text.replace(old_replace, new_replace)

# Fix estimated next episode as well
old_est = "'X': (nextEpNum + 1).toString()"
new_est = "'X': seasonNum > 1 ? '${nextEpNum + 1} (Mùa $seasonNum)' : (nextEpNum + 1).toString()"
text = text.replace(old_est, new_est)

with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated X formatting")

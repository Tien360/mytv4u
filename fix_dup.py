import re

with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    text = f.read()

# The second _progressStickers looks like:
# const Map<String, List<String>> _progressStickers = {
#     'party': ['https://assets4.lottiefiles.com/packages/lf20_touohxv0.json', ...],
#     ...
#     'tense': ['assets/lottie/lf20_m9zragkd.json', 'https://assets10.lottiefiles.com/packages/lf20_pKiaWt.json'],
#   };

# We'll just remove it.
bad_str = """const Map<String, List<String>> _progressStickers = {
  'party': ['https://assets4.lottiefiles.com/packages/lf20_touohxv0.json', 'https://assets5.lottiefiles.com/packages/lf20_dvd9mxbe.json', 'https://assets6.lottiefiles.com/packages/lf20_b8ixs0qm.json'],
  'cry':   ['https://assets2.lottiefiles.com/packages/lf20_ydo1amjm.json', 'https://assets3.lottiefiles.com/packages/lf20_obhph3t0.json', 'assets/lottie/lf20_qp1q7mct.json'],
  'rage':  ['https://assets5.lottiefiles.com/packages/lf20_obhph3t0.json', 'assets/lottie/lf20_5tl1xxnz.json', 'assets/lottie/lf20_syqnfe7c.json'],
  'chill': ['https://assets8.lottiefiles.com/packages/lf20_oqyiaqx4.json', 'https://assets1.lottiefiles.com/packages/lf20_yrtouvgn.json'],
  'tense': ['assets/lottie/lf20_m9zragkd.json', 'https://assets10.lottiefiles.com/packages/lf20_pKiaWt.json'],
};"""

# Wait, spacing might be tricky. Let's use regex to find the one containing http.
text = re.sub(r'const Map<String, List<String>> _progressStickers = \{\s*\'party\': \[\'https://assets4\.lottiefiles.*?\};\s*', '', text, flags=re.DOTALL)

with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(text)

print("Removed duplicate block.")

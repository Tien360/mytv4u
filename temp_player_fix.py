import re

content = open('lib/screens/player_screen.dart', 'r', encoding='utf-8').read()

# Replace 180 with 90 for the popup trigger
content = re.sub(r'\(_duration\.inSeconds - _position\.inSeconds\) <= 180', '(_duration.inSeconds - _position.inSeconds) <= 90', content)

# Fix strings
content = re.sub(r"'Tập tiếp theo sẽ phát sau \ giây'", r"L10n.t('next_ep_in')?.replaceAll('{time}', remaining.toString()) ?? 'Tập tiếp theo sẽ phát sau  giây'", content)
content = re.sub(r"'Phim sẽ đóng sau \ giây'", r"L10n.t('close_in')?.replaceAll('{time}', remaining.toString()) ?? 'Phim sẽ đóng sau  giây'", content)

open('lib/screens/player_screen.dart', 'w', encoding='utf-8').write(content)

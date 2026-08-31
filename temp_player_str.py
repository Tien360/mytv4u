content = open('lib/screens/player_screen.dart', 'r', encoding='utf-8').read()

old_hasNext = """                hasNext
                    ? 'Tập tiếp theo sẽ phát sau $remaining giây'
                    : 'Phim sẽ đóng sau $remaining giây',"""

new_hasNext = """                hasNext
                    ? (L10n.t('next_ep_in')?.replaceAll('{time}', remaining.toString()) ?? 'Tập tiếp theo sẽ phát sau $remaining giây')
                    : (L10n.t('close_in')?.replaceAll('{time}', remaining.toString()) ?? 'Phim sẽ đóng sau $remaining giây'),"""

content = content.replace(old_hasNext, new_hasNext)
open('lib/screens/player_screen.dart', 'w', encoding='utf-8').write(content)

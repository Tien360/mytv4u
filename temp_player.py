import re

for filename in ['lib/screens/player_screen.dart', 'lib/screens/tv_player_screen.dart']:
    content = open(filename, 'r', encoding='utf-8').read()
    
    # 1. Next episode logic: change 5 to 180 (3 minutes)
    content = content.replace("(_duration.inSeconds - _position.inSeconds) <= 5", "(_duration.inSeconds - _position.inSeconds) <= 180")
    
    # 2. _buildNextEpisodeOverlay texts (only in player_screen)
    if 'player_screen' in filename:
        content = content.replace("'Tập tiếp theo sẽ phát sau \ giây'", "L10n.t('next_ep_in')?.replaceAll('{time}', remaining.toString()) ?? 'Tập tiếp theo sẽ phát sau \ giây'")
        content = content.replace("'Phim sẽ đóng sau \ giây'", "L10n.t('close_in')?.replaceAll('{time}', remaining.toString()) ?? 'Phim sẽ đóng sau \ giây'")

    # 3. Dialog Tiêp tục xem texts
    content = content.replace("'Tiếp tục xem?'", "L10n.t('resume_watching') ?? 'Tiếp tục xem?'")
    content = content.replace("'Bạn đã xem đến \. Bạn muốn xem tiếp hay xem lại từ đầu?'", "L10n.t('resume_watching_desc')?.replaceAll('{time}', _formatDuration(Duration(milliseconds: savedPos))) ?? 'Bạn đã xem đến \. Bạn muốn xem tiếp hay xem lại từ đầu?'")
    content = content.replace("'Từ đầu'", "L10n.t('from_start') ?? 'Từ đầu'")
    content = content.replace("'Tiếp tục'", "L10n.t('resume_btn') ?? 'Tiếp tục'")
    # Wait, the screenshot shows "From start" and "Resume", which means it might already be using English text without L10n, or it's using L10n.t('from_start')?
    # I'll just check if it already has L10n.t or what.
    content = content.replace("'From start'", "L10n.t('from_start') ?? 'Từ đầu'")
    content = content.replace("'Resume'", "L10n.t('resume_btn') ?? 'Tiếp tục'")

    open(filename, 'w', encoding='utf-8').write(content)

content = open('lib/screens/library_screen.dart', 'r', encoding='utf-8').read()

content = content.replace("'Mở Link'", "L10n.t('open-link') ?? 'Mở Link'")
content = content.replace("'Mở File'", "L10n.t('open-file') ?? 'Mở File'")
content = content.replace("'Nhập link video/audio (mp4, m3u8, mp3...)'", "L10n.t('open-url-hint') ?? 'Nhập link video/audio/youtube (mp4, m3u8, youtube...)'")

open('lib/screens/library_screen.dart', 'w', encoding='utf-8').write(content)

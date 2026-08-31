import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# default_speed
content = content.replace(
    "Text('Tốc độ mặc định (Default Speed)', style: const TextStyle(color: Colors.white, fontSize: 16))",
    "Text(L10n.t('default_speed') ?? 'Tốc độ mặc định (Default Speed)', style: const TextStyle(color: Colors.white, fontSize: 16))"
)

# background_playback
content = content.replace(
    "Text('Tiếp tục phát âm thanh khi ẩn ứng dụng', style: const TextStyle(color: Colors.white54, fontSize: 13))",
    "Text(L10n.t('background_playback_sub') ?? 'Tiếp tục phát âm thanh khi ẩn ứng dụng', style: const TextStyle(color: Colors.white54, fontSize: 13))"
)

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

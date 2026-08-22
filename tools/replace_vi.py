import re

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    "'Chất lượng video'": "L10n.t('video_quality') ?? 'Chất lượng video'",
    "'Tạm dừng (Space)'": "L10n.t('pause_space') ?? 'Tạm dừng (Space)'",
    "'Phát (Space)'": "L10n.t('play_space') ?? 'Phát (Space)'",
    "'Lùi 10s (←)'": "L10n.t('rewind_10s') ?? 'Lùi 10s (←)'",
    "'Tới 10s (→)'": "L10n.t('forward_10s') ?? 'Tới 10s (→)'",
    "'Âm lượng'": "L10n.t('volume') ?? 'Âm lượng'",
    "'Tập tiếp theo'": "L10n.t('next_ep_tooltip') ?? 'Tập tiếp theo'",
    "'Danh sách tập'": "L10n.t('ep_list_tooltip') ?? 'Danh sách tập'",
    "'Toàn màn hình'": "L10n.t('fullscreen_tooltip') ?? 'Toàn màn hình'",
    "'Trình duyệt Web (Embed)'": "L10n.t('web_browser_embed') ?? 'Trình duyệt Web (Embed)'",
    "'Trình phát Video gốc'": "L10n.t('native_video_player') ?? 'Trình phát Video gốc'",
    "'Luồng bị ngắt kết nối. Vui lòng thử lại!'": "L10n.t('stream_disconnected') ?? 'Luồng bị ngắt kết nối. Vui lòng thử lại!'"
}

for k, v in replacements.items():
    content = content.replace(k, v)
    
with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print('Replaced strings in player_screen.dart')

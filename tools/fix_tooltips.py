import re

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix tooltips
text = re.sub(r"'Đang chọn: \$\{_selectedAudioTrack != null \? _getTrackShortName\(_selectedAudioTrack\) : \"Tự động\"\}'", 
              r"'\\'", text)
text = re.sub(r"'Đang chọn: \$\{_selectedSubtitleTrack != null \? _getTrackShortName\(_selectedSubtitleTrack\) : \"Tự động\"\}'", 
              r"'\\'", text)
text = re.sub(r"'Đang chọn: \$\{_selectedSecondarySubtitleTrack != null \? _getTrackShortName\(_selectedSecondarySubtitleTrack\) : \"Tắt\"\}'", 
              r"'\\'", text)
text = text.replace("tooltip: 'Cài đặt',", "tooltip: L10n.t('settings_tooltip') ?? 'Settings',")

with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated tooltips!")

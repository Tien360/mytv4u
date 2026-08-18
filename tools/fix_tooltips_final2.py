import re

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r"'Đang chọn: \$\{_selectedAudioTrack.*?'", "(L10n.t('currently_selected') ?? 'Selected: ') + (_selectedAudioTrack != null ? _getTrackShortName(_selectedAudioTrack) : (L10n.t('auto') ?? 'Auto'))", text, flags=re.DOTALL)
text = re.sub(r"'Đang chọn: \$\{_selectedSubtitleTrack.*?'", "(L10n.t('currently_selected') ?? 'Selected: ') + (_selectedSubtitleTrack != null ? _getTrackShortName(_selectedSubtitleTrack) : (L10n.t('auto') ?? 'Auto'))", text, flags=re.DOTALL)
text = re.sub(r"'Đang chọn: \$\{_selectedSecondarySubtitleTrack.*?'", "(L10n.t('currently_selected') ?? 'Selected: ') + (_selectedSecondarySubtitleTrack != null ? _getTrackShortName(_selectedSecondarySubtitleTrack) : (L10n.t('off') ?? 'Off'))", text, flags=re.DOTALL)
text = text.replace("tooltip: 'Cài đặt',", "tooltip: L10n.t('settings_tooltip') ?? 'Settings',")

with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

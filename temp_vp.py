content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()
start_idx = content.find("const SizedBox(height: 48)", content.find("_languageKey"))
end_idx = content.find("const SizedBox(height: 48)", content.find("_buildSectionTitle", start_idx))

video_player_code = content[start_idx:end_idx]
print(f"Start: {start_idx}, End: {end_idx}, Length: {len(video_player_code)}")
open('video_player_code.txt', 'w', encoding='utf-8').write(video_player_code)

lines = open('all_settings_replacements.txt', 'r', encoding='utf-8').readlines()
with open('video_player_code.txt', 'w', encoding='utf-8') as f:
    for i in range(4020, 4250):
        f.write(lines[i])

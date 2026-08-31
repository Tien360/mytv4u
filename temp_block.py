lines = open('all_settings_replacements.txt', 'r', encoding='utf-8').readlines()
with open('system_block.txt', 'w', encoding='utf-8') as f:
    for i in range(max(0, 5000), min(len(lines), 5400)):
        f.write(lines[i])

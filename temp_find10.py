lines = open('all_settings_replacements.txt', 'r', encoding='utf-8').readlines()
for i in range(4000, 4200):
    if "auto_next" in lines[i]:
        print(f"Start from {i-50} to {i+50}")
        break

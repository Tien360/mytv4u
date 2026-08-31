lines = open('all_settings_replacements.txt', 'r', encoding='utf-8').readlines()
print(f"File length: {len(lines)}")
print("First 20 lines:")
for i in range(min(20, len(lines))):
    print(lines[i].strip())

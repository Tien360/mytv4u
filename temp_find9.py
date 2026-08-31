lines = open('all_settings_replacements.txt', 'r', encoding='utf-8').readlines()

# Search for the _videoKey section inside the file
for i, line in enumerate(lines):
    if "SizedBox(key: _videoKey)," in line:
        print(f"Found _videoKey at line {i}")

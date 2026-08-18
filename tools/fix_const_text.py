import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    # Remove const before Text
    new_content = re.sub(r'const\s+Text\(', 'Text(', new_content)
    # Remove const before Tooltip if it wraps Tab
    new_content = re.sub(r'const\s+Tooltip\(', 'Tooltip(', new_content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {filepath}")

for root, dirs, files in os.walk('lib'):
    for file in files:
        if file.endswith('.dart'):
            process_file(os.path.join(root, file))


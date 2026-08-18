import os
import re

def contains_vietnamese(s):
    vn_chars = 'áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ'
    vn_chars += vn_chars.upper()
    return any(c in vn_chars for c in s)

def find_hardcoded_strings(dir_path):
    pattern = re.compile(r'(?<!L10n\.t\()([\'"])(.*?)\1')
    results = []
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.dart'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    content = re.sub(r'//.*', '', content)
                    content = re.sub(r'/\*[\s\S]*?\*/', '', content)
                    for m in pattern.finditer(content):
                        s = m.group(2)
                        if contains_vietnamese(s):
                            results.append(f"{file}: {s}")
    
    with open('unlocalized.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))

find_hardcoded_strings('lib')

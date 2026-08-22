import re
with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Check lines that don't have L10n.t but have single quotes
lines = content.split('\n')
for i, line in enumerate(lines):
    if "'" in line and 'L10n.t' not in line and not line.strip().startswith('//'):
        if re.search(r'[àáãạảăắằẳẵặâấầẩẫậèéẹẻẽêềếểễệđìíĩỉịòóõọỏôốồổỗộơớờởỡợùúũụủưứừửữựỳýỵỷỹ]', line, re.IGNORECASE):
            print(f"Line {i+1}: {line.strip()}")

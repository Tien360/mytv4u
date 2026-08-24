import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

parsedName = "Sư Huynh Quá Cẩn Trọng (2026) Pull Strings"
match = re.search(r'^(.*?)\s*\((\d{4})\)\s*(.*)$', parsedName)
if match:
    print("Name:", match.group(1))
    print("Year:", match.group(2))
    print("Original:", match.group(3))
else:
    print("No match")

with open("lib/api/phim_api.dart", "r", encoding="utf-8") as f:
    text = f.read()

import re
match = re.search(r'Future<void> fetchPremium\(\) async \{.*?(?=if \(enabledSources\.contains\(\'motchill\'\)\))', text, re.DOTALL)
if match:
    code = match.group(0)
    open_b = code.count("{")
    close_b = code.count("}")
    print(f"fetchPremium block has {open_b} open braces and {close_b} close braces. Diff: {open_b - close_b}")
else:
    print("Not found")

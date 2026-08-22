with open("tools/release.dart", "r", encoding="utf-8") as f:
    text = f.read()

import re
text = re.sub(r'await stdout\.addStream\(isccProcess\.stdout\);', 
              r'isccProcess.stdout.listen(stdout.add);\n      isccProcess.stderr.listen(stderr.add);', text)
text = re.sub(r'await stdout\.addStream\(ghProcess\.stdout\);', 
              r'ghProcess.stdout.listen(stdout.add);\n      ghProcess.stderr.listen(stderr.add);', text)
text = re.sub(r'final ghPath = .*;', r"final ghPath = 'gh';", text)

with open("tools/release.dart", "w", encoding="utf-8") as f:
    f.write(text)

import re

path = r"t:\Project\Phim\.agents\skills\mytv4u_release\SKILL.md"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace version format logic again to remove zero padding requirement
old_format = r"- \*\*CRITICAL RULE \(Build Promotion\):\*\* The `\[number\]` \(e\.g\., `01`, `02`, `03`\) represents the exact source code snapshot\. \n  - If you build `26\.08\.10\.03\.dev` and it is successful, and the user asks to push it to beta/public, you MUST keep the exact same number: `26\.08\.10\.03\.beta` or `26\.08\.10\.03\.public`\. NEVER reset the number back to `01`\.\n  - Always pad numbers less than 10 with a zero \(`01`, `02`, `09`\) to ensure alphabetical string comparison works flawlessly \(`09` < `10`\)\."

new_format = """- **CRITICAL RULE (Build Promotion):** The `[number]` (e.g., `1`, `2`, `100`) represents the exact source code snapshot. 
  - If you build `26.08.10.3.dev` and it is successful, and the user asks to push it to beta/public, you MUST keep the exact same number: `26.08.10.3.beta` or `26.08.10.3.public`. NEVER reset the number back to `1`.
  - Padding with zeros is NOT required anymore, as the app natively parses numbers in version strings."""

content = re.sub(old_format, new_format, content)

# Replace Example
content = re.sub(r"26\.08\.10\.01\.beta", r"26.08.10.1.beta", content)
content = re.sub(r"26\.08\.10\.03\.beta", r"26.08.10.3.beta", content)

# Replace common mistakes
old_mistake = r"- \*\*Forgetting to update numbers or padding\*\*: If there are multiple releases in one day, increment the number \(`\.01`, `\.02`, `\.03`\)\. Always pad single digits with zero \(`01`, `02`, etc\.\) to prevent string comparison bugs \(e\.g\. '2' is greater than '10' in string math, but '02' is less than '10'\)\."
new_mistake = r"- **Forgetting to increment numbers**: If there are multiple releases in one day, increment the number (`.1`, `.2`, `.100`)."
content = re.sub(old_mistake, new_mistake, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated SKILL.md again.")

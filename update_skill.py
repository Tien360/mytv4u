import re

path = r"t:\Project\Phim\.agents\skills\mytv4u_release\SKILL.md"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace version format logic
old_format = r"- Check the current date. The version format is `YY\.MM\.DD\.\[letter\]\.\[channel\]`\. Example: `26\.08\.10\.a\.beta`\."
new_format = """- Check the current date. The version format is `YY.MM.DD.[number].[channel]`. Example: `26.08.10.01.beta`.
- **CRITICAL RULE (Build Promotion):** The `[number]` (e.g., `01`, `02`, `03`) represents the exact source code snapshot. 
  - If you build `26.08.10.03.dev` and it is successful, and the user asks to push it to beta/public, you MUST keep the exact same number: `26.08.10.03.beta` or `26.08.10.03.public`. NEVER reset the number back to `01`.
  - Always pad numbers less than 10 with a zero (`01`, `02`, `09`) to ensure alphabetical string comparison works flawlessly (`09` < `10`)."""

content = re.sub(old_format, new_format, content)

# Replace Example
old_example = r"dart run tools/release.dart 26\.08\.10\.a\.beta"
new_example = r"dart run tools/release.dart 26.08.10.03.beta"
content = re.sub(old_example, new_example, content)

# Replace common mistakes
old_mistake = r"- \*\*Forgetting to update `\.a`, `\.b` letters\*\*: If there are multiple releases in one day, increment the letter \(e\.g\. `\.a`, `\.b`, `\.c`\)\."
new_mistake = r"- **Forgetting to update numbers or padding**: If there are multiple releases in one day, increment the number (`.01`, `.02`, `.03`). Always pad single digits with zero (`01`, `02`, etc.) to prevent string comparison bugs (e.g. '2' is greater than '10' in string math, but '02' is less than '10')."
content = re.sub(old_mistake, new_mistake, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated SKILL.md successfully.")

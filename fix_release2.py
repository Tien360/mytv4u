import re

with open("tools/release.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Replace Step 4, 5, 6
step4_old = "  // 4. Ä Ã³ng gÃ³i Inno Setup"
step4_new = "  if (!isDev) {\n  // 4. Ä Ã³ng gÃ³i Inno Setup"
if step4_new not in text:
    text = text.replace(step4_old, step4_new)

# Find the end of Firebase try-catch block and close the if(!isDev)
catch_block = "    print('  -> LÃ¡Â»â€”i kÃ¡ÂºÂ¿t nÃ¡Â»â€˜i Firebase: $e');\n  }"
catch_block_new = catch_block + "\n  }"
if catch_block_new not in text:
    text = text.replace(catch_block, catch_block_new)

# Let's fix the end message
text = text.replace("print('\\n=============================================');", "if (isDev) { print('🎉 Da Hoan Tat Ban DEV (Bo qua Inno Setup & Firebase)!'); } else {")
text = text.replace("print('=============================================');\n}", "print('=============================================');\n}\n}")

with open("tools/release.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated release.dart")

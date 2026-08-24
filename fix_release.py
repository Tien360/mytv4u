import re

with open("tools/release.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Insert isDev variable
is_dev_code = "  final notes = args[1];\n  final bool isDev = version.contains('.dev');\n"
text = text.replace("  final notes = args[1];\n", is_dev_code)

# Replace Step 2
step2_old = "  // 2. CÃ¡ÂºÂ­p nhÃ¡ÂºÂ­t installer.iss"
step2_new = "  // 2. CÃ¡ÂºÂ­p nhÃ¡ÂºÂ­t installer.iss\n  if (!isDev) {"
text = text.replace(step2_old, step2_new)

# Close Step 2 before Step 3
step3_old = "  // 3. ChÃ¡ÂºÂ¡y Flutter Build"
step3_new = "  }\n\n  // 3. ChÃ¡ÂºÂ¡y Flutter Build"
text = text.replace(step3_old, step3_new)

# Replace Step 4, 5, 6
step4_old = "  // 4. Ä Ã³ng gÃ³i Inno Setup"
step4_new = "  if (!isDev) {\n  // 4. Ä Ã³ng gÃ³i Inno Setup"
text = text.replace(step4_old, step4_new)

# Close the big if block before the success print
success_print_old = "  print('\\n=============================================');\n  print('Ã°Å¸Å½â€° Ã„Â ÃƒÆ’ HOÃƒâ‚¬N TÃ¡ÂºÂ¤T TOÃƒâ‚¬N BÃ¡Â»Ëœ QUÃƒÂ  TRÃƒÅ’NH PHÃƒÂ T HÃƒâ‚¬NH! Ã°Å¸Å½â€°');"
success_print_new = "  }\n\n" + success_print_old
text = text.replace(success_print_old, success_print_new)

# Also update the success message to indicate if it was dev
dev_success_print = """
  print('\\n=============================================');
  if (isDev) {
    print('🎉 ĐÃ HOÀN TẤT BIÊN DỊCH BẢN DEV (Bỏ qua Đóng gói & Phát hành)! 🎉');
    print('File thực thi tại: build/windows/x64/runner/Release/MyTV4U.exe');
  } else {
    print('🎉 ĐÃ HOÀN TẤT TOÀN BỘ QUÁ TRÌNH PHÁT HÀNH! 🎉');
    print('Đường dẫn file: $setupExePath');
  }
  print('=============================================');
}"""

# Replace the end block entirely to fix character encoding issues and add the nice branch.
# We'll use regex to replace from "print('\n=============================================');" to the end of the file.
text = re.sub(r"  print\('\\n============================================='\);\s*print\('.*?HOÃƒâ‚¬N TÃ¡ÂºÂ¤T.*?'\);\s*print\('Ã„Â Ã†Â°Ã¡Â»Â ng dÃ¡ÂºÂ«n file: \$setupExePath'\);\s*print\('============================================='\);\s*}", dev_success_print, text, flags=re.DOTALL)

with open("tools/release.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated release.dart")

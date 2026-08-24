import re

with open("tools/release.dart", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Insert isDev
text = text.replace("  final notes = args[1];\n", "  final notes = args[1];\n  final bool isDev = version.contains('.dev');\n")

# 2. Step 2 wrap
text = text.replace("  // 2. CÃ¡ÂºÂ­p nhÃ¡ÂºÂ­t installer.iss", "  // 2. CÃ¡ÂºÂ­p nhÃ¡ÂºÂ­t installer.iss\n  if (!isDev) {")
text = text.replace("  // 3. ChÃ¡ÂºÂ¡y Flutter Build", "  }\n\n  // 3. ChÃ¡ÂºÂ¡y Flutter Build")

# 3. Step 4, 5, 6 wrap
text = text.replace("  // 4. Ä Ã³ng gÃ³i Inno Setup", "  if (!isDev) {\n  // 4. Ä Ã³ng gÃ³i Inno Setup")

# Close Step 4, 5, 6
# Look for the last catch block ending, before the print footer
text = text.replace("    print('  -> LÃ¡Â»â€”i kÃ¡ÂºÂ¿t nÃ¡Â»â€˜i Firebase: $e');\n  }\n\n  print('\\n=============================================');",
                    "    print('  -> LÃ¡Â»â€”i kÃ¡ÂºÂ¿t nÃ¡Â»â€˜i Firebase: $e');\n  }\n  }\n\n  print('\\n=============================================');")

# 4. Modify Footer
footer_old = """  print('\\n=============================================');
  print('Ã°Å¸Å½â€° Ã„Â ÃƒÆ’ HOÃƒâ‚¬N TÃ¡ÂºÂ¤T TOÃƒâ‚¬N BÃ¡Â»Ëœ QUÃƒÂ  TRÃƒÅ’NH PHÃƒÂ T HÃƒâ‚¬NH! Ã°Å¸Å½â€°');
  print('Ã„Â Ã†Â°Ã¡Â»Â ng dÃ¡ÂºÂ«n file: $setupExePath');
  print('=============================================');
}"""

footer_new = """  print('\\n=============================================');
  if (isDev) {
    print('🎉 ĐÃ HOÀN TẤT BIÊN DỊCH BẢN DEV (Bỏ qua Đóng gói & Phát hành)! 🎉');
    print('File thực thi tại: build/windows/x64/runner/Release/MyTV4U.exe');
  } else {
    print('🎉 ĐÃ HOÀN TẤT TOÀN BỘ QUÁ TRÌNH PHÁT HÀNH! 🎉');
    print('Đường dẫn file: $setupExePath');
  }
  print('=============================================');
}"""
text = text.replace(footer_old, footer_new)

with open("tools/release.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated successfully")

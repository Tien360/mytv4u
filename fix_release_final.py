with open("tools/release.dart", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Add isDev
text = text.replace("final notes = args[1];", "final notes = args[1];\n  final bool isDev = version.contains('.dev');")

# 2. Add if(!isDev) around step 2
step2_start = text.find("// 2. CÃ¡ÂºÂ­p")
step3_start = text.find("// 3. ChÃ¡ÂºÂ¡y")

step2_block = text[step2_start:step3_start]
step2_new = "if (!isDev) {\n  " + step2_block.replace("\n", "\n  ").strip() + "\n  }\n\n  "
text = text.replace(step2_block, step2_new)

# 3. Add if(!isDev) around step 4,5,6
step4_start = text.find("// 4. Ä Ã³ng gÃ³i")
footer_start = text.find("print('\\n=============================================');")

steps_block = text[step4_start:footer_start]
steps_new = "if (!isDev) {\n  " + steps_block.replace("\n", "\n  ").strip() + "\n  }\n\n  "
text = text.replace(steps_block, steps_new)

# 4. Modify Footer
footer_old = text[footer_start:]

footer_new = """print('\\n=============================================');
  if (isDev) {
    print('🎉 ĐÃ HOÀN TẤT BIÊN DỊCH BẢN DEV (Bỏ qua Đóng gói & Phát hành)! 🎉');
    print('File thực thi tại: build/windows/x64/runner/Release/MyTV4U.exe');
  } else {
    print('🎉 ĐÃ HOÀN TẤT TOÀN BỘ QUÁ TRÌNH PHÁT HÀNH! 🎉');
    print('Đường dẫn file: $setupExePath');
  }
  print('=============================================');
}
"""
text = text.replace(footer_old, footer_new)

with open("tools/release.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated beautifully")

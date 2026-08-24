with open("tools/release.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

out = []
is_dev_written = False

in_step2 = False
in_step4 = False

for line in lines:
    if "final notes = args[1];" in line:
        out.append(line)
        out.append("  final bool isDev = version.contains('.dev');\n")
        continue
    
    if "// 2." in line and "installer.iss" in line:
        out.append("  if (!isDev) {\n")
        out.append(line)
        in_step2 = True
        continue
        
    if "// 3." in line and "Flutter Build" in line:
        if in_step2:
            out.append("  }\n\n")
            in_step2 = False
        out.append(line)
        continue
        
    if "// 4." in line and "Inno Setup" in line:
        out.append("  if (!isDev) {\n")
        out.append(line)
        in_step4 = True
        continue
        
    if "print('\\n=============================================');" in line:
        if in_step4:
            out.append("  }\n")
            in_step4 = False
        
        # Write custom footer
        out.append("  print('\\n=============================================');\n")
        out.append("  if (isDev) {\n")
        out.append("    print('🎉 ĐÃ HOÀN TẤT BIÊN DỊCH BẢN DEV (Bỏ qua Đóng gói & Phát hành)! 🎉');\n")
        out.append("    print('File thực thi tại: build/windows/x64/runner/Release/MyTV4U.exe');\n")
        out.append("  } else {\n")
        out.append("    print('🎉 ĐÃ HOÀN TẤT TOÀN BỘ QUÁ TRÌNH PHÁT HÀNH! 🎉');\n")
        out.append("    print('Đường dẫn file: $setupExePath');\n")
        out.append("  }\n")
        out.append("  print('=============================================');\n")
        out.append("}\n")
        break
        
    out.append(line)

with open("tools/release.dart", "w", encoding="utf-8") as f:
    f.writelines(out)
print("Updated successfully")

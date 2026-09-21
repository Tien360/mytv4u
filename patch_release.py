
with open("tools/release.dart", "r", encoding="utf-8") as f:
    text = f.read()

target = "print('  -> Đã sao chép tv_web_player thành công!');\n  }"
if target in text:
    replacement = target + """\n\n  final tvWebPlayerNguonCDir = Directory(r\"..\\tv_web_player_nguonc\\bin\\Release\\net8.0-windows\\win-x64\\publish\");\n  if (tvWebPlayerNguonCDir.existsSync()) {\n    await Process.run(\"xcopy\", [r\"..\\tv_web_player_nguonc\\bin\\Release\\net8.0-windows\\win-x64\\publish\\*\", r\"build\\windows\\x64\\runner\\Release\\\", \"/E\", \"/I\", \"/Y\"]);\n    print('  -> Đã sao chép tv_web_player_nguonc thành công!');\n  }"""
    text = text.replace(target, replacement)
    print("Replaced successfully")
else:
    print("Not found.")

with open("tools/release.dart", "w", encoding="utf-8") as f:
    f.write(text)

with open("tools/release.dart", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("final bool isDev = version.contains('.dev');", "final bool isDev = version.contains('.dev');\n  final setupExePath = 'Releases\\\\v$version\\\\MyTV4U_Setup_$version.exe';")

with open("tools/release.dart", "w", encoding="utf-8") as f:
    f.write(text)

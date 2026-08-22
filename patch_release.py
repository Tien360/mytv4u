import re

with open('tools/release.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the part where it prepares files for Inno Setup or just before creating the installer
# Actually, the easiest way is to add it after "build windows" is done.
patch = r"""
  print('[3/6] Sao chép audio.ico...');
  final audioIcoSrc = File('windows/runner/resources/audio.ico');
  final audioIcoDest = File('build/windows/x64/runner/Release/audio.ico');
  if (audioIcoSrc.existsSync()) {
    audioIcoSrc.copySync(audioIcoDest.path);
  }
"""

if "Sao chép audio.ico" not in content:
    content = re.sub(r'(print\(\'\[3/6\] Đóng gói installer...\'\);)', patch + r'\n  \1', content)
    with open('tools/release.dart', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated release.dart")

import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

bad_str = """                                  Row(
                                    mainAxisAlignment:
                                        MainAxisAlignment.spaceBetween,
                                    children: [
                                      const SizedBox(height: 48),
                                  SizedBox(key: _audioKey),"""

good_str = """                                  const SizedBox(height: 48),
                                  SizedBox(key: _audioKey),"""

content = content.replace(bad_str, good_str)

bad_str2 = """                                  const SizedBox(height: 48),
                                  SizedBox(key: _sourcesKey),
                                      _buildSectionTitle("""

good_str2 = """                                  const SizedBox(height: 48),
                                  SizedBox(key: _sourcesKey),
                                  Row(
                                    mainAxisAlignment:
                                        MainAxisAlignment.spaceBetween,
                                    children: [
                                      _buildSectionTitle("""

content = content.replace(bad_str2, good_str2)

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed layout!")

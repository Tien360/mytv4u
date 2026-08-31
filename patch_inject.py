path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "_buildLoginCard()," in line:
        # Check if we already injected
        if "_buildYouTubeLinkCard()" not in lines[i+1] and "_buildYouTubeLinkCard()" not in lines[i+2]:
            lines.insert(i+1, "                                  const SizedBox(height: 16),\n                                  _buildYouTubeLinkCard(),\n")
        break

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Injected call successfully")

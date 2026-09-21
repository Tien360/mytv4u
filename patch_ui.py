import re

with open("lib/screens/yt_player_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Replace method contents with empty container to avoid errors
content = re.sub(r"Widget _buildNextEpisodeOverlay\(\) \{.*?return Container\(.*?\);\n    \}\n", "Widget _buildNextEpisodeOverlay() { return SizedBox.shrink(); }", content, flags=re.DOTALL)
content = re.sub(r"Widget _buildPremiumBadges\(\) \{.*?return Wrap\(.*?\);\n    \}\n", "Widget _buildPremiumBadges() { return SizedBox.shrink(); }", content, flags=re.DOTALL)
content = re.sub(r"Widget _buildMotchillServerList\(\) \{.*?return Column\(.*?\);\n    \}\n", "Widget _buildMotchillServerList() { return SizedBox.shrink(); }", content, flags=re.DOTALL)

with open("lib/screens/yt_player_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)

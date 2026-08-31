import re

with open('lib/screens/tv_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Add import
if 'package:cached_network_image/cached_network_image.dart' not in content:
    content = content.replace(
        "import '../utils/l10n.dart';",
        "import '../utils/l10n.dart';\nimport 'package:cached_network_image/cached_network_image.dart';"
    )

# Replace _buildChannelLogo
old_func_start = '''  Widget _buildChannelLogo() {
    final id = widget.channel.id.toLowerCase();

    // Custom High-Quality Branded Badges for each TV station'''

new_func_start = '''  Widget _buildChannelLogo() {
    if (widget.channel.logo.isNotEmpty) {
      return CachedNetworkImage(
        imageUrl: widget.channel.logo,
        height: 60,
        fit: BoxFit.contain,
        placeholder: (context, url) => const CircularProgressIndicator(color: Color(0xFF3B82F6)),
        errorWidget: (context, url, error) => _buildFallbackLogo(),
      );
    }
    return _buildFallbackLogo();
  }

  Widget _buildFallbackLogo() {
    final id = widget.channel.id.toLowerCase();

    // Custom High-Quality Branded Badges for each TV station'''

content = content.replace(old_func_start, new_func_start)

with open('lib/screens/tv_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched tv_screen.dart successfully!")

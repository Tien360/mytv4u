import re

with open('lib/widgets/advanced_controls_panel.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Rename class
content = content.replace('AdvancedControlsPanel', 'AdvancedControlsTab')
content = content.replace('final VoidCallback onClose;', '')
content = content.replace('required this.onClose,', '')

# Remove GlassContainer and Header
new_build = '''  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
'''

content = re.sub(r'  @override\s+Widget build\(BuildContext context\) \{.*?(?=const Text\(\'Màu sắc Video\')', new_build, content, flags=re.DOTALL)

# Remove the trailing ), ], ), ); } from GlassContainer
content = content.replace('            ),\n          ),\n        ],\n      ),\n    );', '      ),\n    );')

with open('lib/widgets/advanced_controls_panel.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print('Patched AdvancedControlsTab')

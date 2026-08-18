import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

old_item = '''  Widget _buildSidebarItem(String title, IconData icon, GlobalKey targetKey) {
    return ListTile(
      leading: Icon(icon, color: Colors.white70),
      title: Text(title, style: const TextStyle(color: Colors.white70)),
      onTap: () {
        if (targetKey.currentContext != null) {
          Scrollable.ensureVisible(
            targetKey.currentContext!,
            duration: const Duration(milliseconds: 500),
            curve: Curves.easeInOut,
            alignment: 0.0,
          );
        }
      },
    );
  }'''

new_item = '''  Widget _buildSidebarItem(String title, IconData icon, GlobalKey targetKey) {
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 4, horizontal: 12),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(12),
          hoverColor: Colors.white10,
          onTap: () {
            if (targetKey.currentContext != null) {
              Scrollable.ensureVisible(
                targetKey.currentContext!,
                duration: const Duration(milliseconds: 500),
                curve: Curves.easeInOut,
                alignment: 0.0,
              );
            }
          },
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            child: Row(
              children: [
                Icon(icon, color: Colors.white70, size: 22),
                const SizedBox(width: 14),
                Text(
                  title,
                  style: const TextStyle(
                    color: Colors.white70,
                    fontWeight: FontWeight.w500,
                    fontSize: 15,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }'''

text = text.replace(old_item, new_item)

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated _buildSidebarItem in settings_screen.dart")

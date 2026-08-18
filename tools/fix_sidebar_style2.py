import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# We need to replace the _buildSidebarItem function robustly
match = re.search(r'  Widget _buildSidebarItem.*?^  Widget _buildSidebarMenu', text, re.MULTILINE | re.DOTALL)
if match:
    old_func = match.group(0)
    new_func = '''  Widget _buildSidebarItem(String title, IconData icon, GlobalKey keyTarget) {
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 4, horizontal: 12),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(12),
          hoverColor: Colors.white10,
          onTap: () {
            _scrollTo(keyTarget);
            if (MediaQuery.of(context).size.width < 800) {
               Navigator.pop(context); // close drawer on mobile
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
  }

  Widget _buildSidebarMenu'''
    
    text = text.replace(old_func, new_func)
    
    with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced successfully")
else:
    print("Could not find the function")

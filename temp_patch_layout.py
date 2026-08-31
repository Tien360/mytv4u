import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix _buildUserCard
# Currently it is: child: Row( \n children: [ \n CircleAvatar ... OutlinedButton ... Divider ... YouTube Row ]
# We need to wrap it in a Column and close the first Row before the Divider.

user_search = """    return GlassContainer(
      padding: const EdgeInsets.all(20),
      borderRadius: 16,
      child: Row(
        children: ["""

user_replace = """    return GlassContainer(
      padding: const EdgeInsets.all(20),
      borderRadius: 16,
      child: Column(
        children: [
          Row(
            children: ["""

idx_user = content.find(user_search)
if idx_user != -1:
    content = content[:idx_user] + user_replace + content[idx_user+len(user_search):]
    # Now find the Divider inside _buildUserCard and close the Row before it
    div_search = """          const Padding(
            padding: EdgeInsets.symmetric(vertical: 8),
            child: Divider(color: Colors.white10),
          ),
          // YouTube"""
    
    div_replace = """            ],
          ),
          const Padding(
            padding: EdgeInsets.symmetric(vertical: 16),
            child: Divider(color: Colors.white10),
          ),
          // YouTube"""
    
    idx_div1 = content.find(div_search, idx_user)
    if idx_div1 != -1:
        content = content[:idx_div1] + div_replace + content[idx_div1+len(div_search):]
        print("Fixed _buildUserCard layout!")

# Fix _buildLoginCard
login_search = """    return GlassContainer(
      padding: const EdgeInsets.all(20),
      borderRadius: 16,
      child: Row(
        children: ["""
        
idx_login = content.find(login_search, idx_user + 500)
if idx_login != -1:
    content = content[:idx_login] + user_replace + content[idx_login+len(login_search):]
    idx_div2 = content.find(div_search, idx_login)
    if idx_div2 != -1:
        content = content[:idx_div2] + div_replace + content[idx_div2+len(div_search):]
        print("Fixed _buildLoginCard layout!")

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

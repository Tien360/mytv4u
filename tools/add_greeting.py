import sys
import re

with open('lib/screens/home_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Add _userName
text = text.replace("bool _isLoggedIn = false;", "bool _isLoggedIn = false;\n  String? _userName;")

# Update _loadHistory
old_history = '''  Future<void> _loadHistory() async {
    final user = await AuthApi.getCurrentUser();
    if (user != null) {
      _isLoggedIn = true;
    }
    // Always load history, even anonymously'''
new_history = '''  Future<void> _loadHistory() async {
    final user = await AuthApi.getCurrentUser();
    if (user != null) {
      _isLoggedIn = true;
      _userName = user['name'];
    } else {
      _isLoggedIn = false;
      _userName = null;
    }
    // Always load history, even anonymously'''
text = text.replace(old_history, new_history)

# Update ListView
old_list = '''        child: ListView.builder(
          controller: _scrollController,
          itemCount: _sections.length + 2, // Hero + History + Sections
          itemBuilder: (context, index) {
            if (index == 0) return _buildHeroCarousel();
            if (index == 1) return _buildHistorySection();
            
            final section = _sections[index - 2];'''
new_list = '''        child: ListView.builder(
          controller: _scrollController,
          itemCount: _sections.length + 3, // Header + Hero + History + Sections
          itemBuilder: (context, index) {
            if (index == 0) return _buildGreetingHeader();
            if (index == 1) return _buildHeroCarousel();
            if (index == 2) return _buildHistorySection();
            
            final section = _sections[index - 3];'''
text = text.replace(old_list, new_list)

# Inject _buildGreetingHeader
header_code = '''  Widget _buildGreetingHeader() {
    if (!_isLoggedIn || _userName == null) return const SizedBox.shrink();
    return Padding(
      padding: const EdgeInsets.only(left: 32, right: 32, top: 24, bottom: 16),
      child: Row(
        children: [
          Image.asset('assets/logo.png', height: 40),
          const SizedBox(width: 16),
          Text(
            '\ !',
            style: const TextStyle(
              color: Colors.white,
              fontSize: 26,
              fontWeight: FontWeight.bold,
              letterSpacing: 0.5,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHeroCarousel() {'''
text = text.replace("  Widget _buildHeroCarousel() {", header_code)

with open('lib/screens/home_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated home_screen.dart!")

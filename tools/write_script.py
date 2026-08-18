import os
import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Add GlobalKeys
keys = '''
  final GlobalKey _accountKey = GlobalKey();
  final GlobalKey _colorKey = GlobalKey();
  final GlobalKey _subtitleKey = GlobalKey();
  final GlobalKey _systemKey = GlobalKey();
  final GlobalKey _sourcesKey = GlobalKey();
  final GlobalKey _infoKey = GlobalKey();
  
  final ScrollController _scrollController = ScrollController();

  void _scrollTo(GlobalKey key) {
    if (key.currentContext != null) {
      Scrollable.ensureVisible(
        key.currentContext!,
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
      );
    }
  }
'''

# Insert keys after ool _backgroundPlayback = false;
text = text.replace('bool _backgroundPlayback = false;', 'bool _backgroundPlayback = false;\n' + keys)

# Let's inject Keys to the Sections:
text = text.replace("_buildSectionTitle(Icons.account_circle, L10n.t('sync_account')),",
                    "SizedBox(key: _accountKey),\n_buildSectionTitle(Icons.account_circle, L10n.t('sync_account')),")

text = text.replace("_buildSectionTitle(Icons.color_lens, L10n.t('global_color_settings') ?? 'Cài đặt màu toàn cục'),",
                    "SizedBox(key: _colorKey),\n_buildSectionTitle(Icons.color_lens, L10n.t('global_color_settings') ?? 'Cài đặt màu toàn cục'),")

text = text.replace("_buildSectionTitle(Icons.subtitles, L10n.t('subtitles')),",
                    "SizedBox(key: _subtitleKey),\n_buildSectionTitle(Icons.subtitles, L10n.t('subtitles')),")

text = text.replace("_buildSectionTitle(Icons.settings_suggest, L10n.t('health_utilities')),",
                    "SizedBox(key: _systemKey),\n_buildSectionTitle(Icons.settings_suggest, L10n.t('health_utilities')),")

text = text.replace("_buildSectionTitle(Icons.source, L10n.t('sources')),",
                    "SizedBox(key: _sourcesKey),\n_buildSectionTitle(Icons.source, L10n.t('sources')),")

text = text.replace("_buildSectionTitle(Icons.info_outline, L10n.t('info_contact')),",
                    "SizedBox(key: _infoKey),\n_buildSectionTitle(Icons.info_outline, L10n.t('info_contact')),")


# Rewrite the build method header.
# Currently it is:
'''
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF000000),
      body: Stack(
        children: [
          SafeArea(
            child: Column(
              children: [
                // Custom Header with Top Padding
                ...
            Expanded(
              child: ListView(
                padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                children: [
                  Center(
                    child: ConstrainedBox(
                      constraints: const BoxConstraints(maxWidth: 800),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
'''

new_build_header = '''
  Widget _buildSidebarItem(String title, IconData icon, GlobalKey keyTarget) {
    return ListTile(
      leading: Icon(icon, color: Colors.white70),
      title: Text(title, style: const TextStyle(color: Colors.white70)),
      onTap: () {
        _scrollTo(keyTarget);
        if (MediaQuery.of(context).size.width < 800) {
           Navigator.pop(context); // close drawer on mobile
        }
      },
    );
  }

  Widget _buildSidebarMenu() {
    return ListView(
      padding: const EdgeInsets.symmetric(vertical: 24),
      children: [
        _buildSidebarItem(L10n.t('sync_account') ?? 'Tài khoản', Icons.account_circle, _accountKey),
        _buildSidebarItem(L10n.t('global_color_settings') ?? 'Màu sắc', Icons.color_lens, _colorKey),
        _buildSidebarItem(L10n.t('subtitles') ?? 'Phụ đề', Icons.subtitles, _subtitleKey),
        _buildSidebarItem(L10n.t('health_utilities') ?? 'Hệ thống', Icons.settings_suggest, _systemKey),
        _buildSidebarItem(L10n.t('sources') ?? 'Nguồn phim', Icons.source, _sourcesKey),
        _buildSidebarItem(L10n.t('info_contact') ?? 'Thông tin', Icons.info_outline, _infoKey),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    final isDesktop = MediaQuery.of(context).size.width >= 800;

    return Scaffold(
      backgroundColor: const Color(0xFF000000),
      drawer: isDesktop ? null : Drawer(
        backgroundColor: const Color(0xFF1A1A1A),
        child: SafeArea(child: _buildSidebarMenu()),
      ),
      body: Stack(
        children: [
          SafeArea(
            child: Row(
              children: [
                if (isDesktop)
                  Container(
                    width: 250,
                    color: Colors.white.withOpacity(0.02),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Padding(
                          padding: const EdgeInsets.all(24.0),
                          child: Row(
                            children: [
                              IconButton(
                                icon: const Icon(Icons.arrow_back, color: Colors.white),
                                onPressed: () => Navigator.pop(context),
                              ),
                              const SizedBox(width: 8),
                              Expanded(
                                child: Text(L10n.t('settings'), style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white)),
                              ),
                            ],
                          ),
                        ),
                        Expanded(child: _buildSidebarMenu()),
                      ],
                    ),
                  ),
                
                Expanded(
                  child: Column(
                    children: [
                      if (!isDesktop)
                        Padding(
                          padding: const EdgeInsets.only(top: 16.0, left: 16.0, right: 16.0, bottom: 8.0),
                          child: Row(
                            children: [
                              Builder(
                                builder: (ctx) => Container(
                                  decoration: BoxDecoration(color: Colors.white.withOpacity(0.05), shape: BoxShape.circle),
                                  child: IconButton(
                                    icon: const Icon(Icons.menu, color: Colors.white, size: 24),
                                    onPressed: () => Scaffold.of(ctx).openDrawer(),
                                  ),
                                ),
                              ),
                              const SizedBox(width: 16),
                              Container(
                                decoration: BoxDecoration(color: Colors.white.withOpacity(0.05), shape: BoxShape.circle),
                                child: IconButton(
                                  icon: const Icon(Icons.arrow_back, color: Colors.white, size: 24),
                                  onPressed: () => Navigator.pop(context),
                                ),
                              ),
                              const SizedBox(width: 16),
                              Text(L10n.t('settings'), style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white)),
                            ],
                          ),
                        ),
                      
                      Expanded(
                        child: SingleChildScrollView(
                          controller: _scrollController,
                          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                          child: Center(
                            child: ConstrainedBox(
                              constraints: const BoxConstraints(maxWidth: 800),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
'''

old_build_header = text[text.find('  @override\n  Widget build(BuildContext context) {'):text.find('_buildSectionTitle(Icons.account_circle')]
text = text.replace(old_build_header, new_build_header)

# Fix missing closing tags at the very end
# Current end of build is:
'''
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          
          if (_isLoadingAppInfo || _isLoggingIn)
            Container(
              color: Colors.black54,
              child: const Center(
                child: CircularProgressIndicator(color: Color(0xFFE50914)),
              ),
            ),
        ],
      ),
    );
  }
'''
new_build_footer = '''
                        ],
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
'''

# Wait, the footer logic needs careful replacement because there are extra/fewer brackets now.
# Let's count bracket depth in python instead or just replace from the bottom.

'''

text = text.replace("_buildSectionTitle(Icons.color_lens, L10n.t('global_color_settings') ?? 'CÃ\xa0i Ä\x91áº·t mÃ\xa0u toÃ\xa0n cá»¥c')", "_buildSectionTitle(Icons.color_lens, L10n.t('global_color_settings'))")


with open('tools/refactor_settings.py', 'w', encoding='utf-8') as f:
    f.write(text)


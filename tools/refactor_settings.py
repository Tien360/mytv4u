import os

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_build = False

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
'''

build_header_new = '''
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

skip_until_children = False
closing_tags_count = 0

for i, line in enumerate(lines):
    if line.strip() == 'bool _backgroundPlayback = false;':
        new_lines.append(line)
        new_lines.append(keys)
        continue
    
    if line.strip() == '@override' and lines[i+1].strip().startswith('Widget build(BuildContext context)'):
        in_build = True
        new_lines.append(build_header_new)
        skip_until_children = True
        continue
        
    if skip_until_children:
        if 'children: [' in line and 'crossAxisAlignment: CrossAxisAlignment.start' in lines[i-1]:
            skip_until_children = False
        continue
        
    # Inject GlobalKeys
    if in_build:
        if "_buildSectionTitle(Icons.account_circle, L10n.t('sync_account'))" in line:
            new_lines.append('SizedBox(key: _accountKey),\n')
        elif "_buildSectionTitle(Icons.color_lens, L10n.t('global_color_settings')" in line:
            new_lines.append('SizedBox(key: _colorKey),\n')
            line = line.replace("?? 'Cài đặt màu toàn cục'", "") # cleanup
        elif "_buildSectionTitle(Icons.subtitles, L10n.t('subtitles'))" in line:
            new_lines.append('SizedBox(key: _subtitleKey),\n')
        elif "_buildSectionTitle(Icons.settings_suggest, L10n.t('health_utilities'))" in line:
            new_lines.append('SizedBox(key: _systemKey),\n')
        elif "_buildSectionTitle(Icons.source, L10n.t('sources'))" in line:
            new_lines.append('SizedBox(key: _sourcesKey),\n')
        elif "_buildSectionTitle(Icons.info_outline, L10n.t('info_contact'))" in line:
            new_lines.append('SizedBox(key: _infoKey),\n')

    # Wait, the closing brackets at the end of the file.
    # The old structure was Scaffold > Stack > SafeArea > Column > Expanded > ListView > Center > ConstrainedBox > Column
    # New structure is Scaffold > Stack > SafeArea > Row > Expanded > Column > Expanded > SingleChildScrollView > Center > ConstrainedBox > Column
    # So we need one more bracket at the end. Or I can just leave it alone if I just replaced ListView with SingleChildScrollView?
    # Old: Column > Expanded > ListView > children
    # New: Column > Expanded > SingleChildScrollView > Center > ConstrainedBox > Column > children
    # Wait, the old structure ALREADY had Center > ConstrainedBox > Column.
    # Let me check the old structure again.
    new_lines.append(line)

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)


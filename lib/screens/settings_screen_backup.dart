import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../api/auth_api.dart';
import '../api/firebase_api.dart';
import '../widgets/glass_container.dart';
import '../widgets/custom_title_bar.dart';
import '../api/update_api.dart';
import '../widgets/update_dialog.dart';
import '../utils/l10n.dart';
import '../utils/ui_utils.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  Map<String, String>? _currentUser;
  bool _isLoggingIn = false;
  
  Map<String, dynamic>? _appSettings;
  bool _isLoadingAppInfo = true;
  bool _hwAccel = true;
  double _subSize = 24.0;
  double _subOpacity = 0.3;
  String _subColor = 'White';
  String _subFont = 'Roboto';
  bool _autoNext = true;
  bool _autoPlayTrailer = true;
  double _defaultSpeed = 1.0;
  int _watchLimit = 0;
  String _appLang = 'vi';

  // Nguồn phim mặc định
  final Map<String, bool> _sources = {
    'premium': true,
    'nguonc': true,
    'ophim': true,
    'kkphim': true,
    'vsmov': true,
    'phim4k': true,
    'free1': true,
    'motchill': true,
    'torrentio': false, // Torrent is experimental, default to off
  };

  @override
  void initState() {
    super.initState();
    _loadSettings();
    _loadAppInfo();
  }

  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    
    // Tải cấu hình nguồn phim
    final enabledSources = prefs.getStringList('enabled_sources');
    if (enabledSources != null) {
      setState(() {
        for (var key in _sources.keys) {
          _sources[key] = enabledSources.contains(key);
        }
      });
    }

    // Tải cấu hình GPU, Subtitle & Tiện ích
    if (mounted) {
      setState(() {
        _hwAccel = prefs.getBool('enable_hw_accel') ?? true;
        _subSize = prefs.getDouble('sub_size') ?? 24.0;
        _subOpacity = prefs.getDouble('sub_opacity') ?? 0.3;
        _subColor = prefs.getString('sub_color') ?? 'White';
        _subFont = prefs.getString('sub_font') ?? 'Roboto';
        _autoNext = prefs.getBool('auto_next') ?? true;
        _autoPlayTrailer = prefs.getBool('auto_play_trailer') ?? true;
        _defaultSpeed = prefs.getDouble('default_speed') ?? 1.0;
        _watchLimit = prefs.getInt('watch_limit') ?? 0;
        _appLang = prefs.getString('app_lang') ?? 'vi';
      });
    }

    // Tải user
    final user = await AuthApi.getCurrentUser();
    if (mounted && user != null) {
      setState(() {
        _currentUser = user;
      });
    }
  }

  Future<void> _loadAppInfo() async {
    final info = await FirebaseApi.getAppSettings();
    if (mounted) {
      setState(() {
        _appSettings = info ?? {
          'developer': 'Sparky',
          'contact': 'mytv4u.web.app',
          'version': UpdateApi.currentAppVersion,
          'facebook': '',
        };
        _isLoadingAppInfo = false;
      });
    }
  }

  Future<void> _saveSources() async {
    final prefs = await SharedPreferences.getInstance();
    final enabledList = _sources.entries.where((e) => e.value).map((e) => e.key).toList();
    await prefs.setStringList('enabled_sources', enabledList);
  }

  Future<void> _handleLogin() async {
    setState(() => _isLoggingIn = true);
    final user = await AuthApi.loginWithGoogle();
    if (mounted) {
      setState(() {
        _isLoggingIn = false;
        if (user != null) {
          _currentUser = user;
        }
      });
    }
  }

  Future<void> _handleLogout() async {
    await AuthApi.logout();
    setState(() {
      _currentUser = null;
    });
  }

  Color _getColorFromName(String name) {
    switch (name.toLowerCase()) {
      case 'yellow': return Colors.yellow;
      case 'green': return Colors.greenAccent;
      case 'cyan': return Colors.cyanAccent;
      default: return Colors.white;
    }
  }

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
                Padding(
                  padding: const EdgeInsets.only(top: 48.0, left: 16.0, right: 16.0, bottom: 8.0),
                  child: Row(
                    children: [
                      Container(
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.05),
                          shape: BoxShape.circle,
                        ),
                        child: IconButton(
                          icon: const Icon(Icons.arrow_back, color: Colors.white, size: 24),
                          onPressed: () => Navigator.pop(context),
                        ),
                      ),
                      const SizedBox(width: 16),
                      Text(
                        L10n.t('settings'),
                        style: const TextStyle(
                          fontSize: 28,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                          letterSpacing: 0.5,
                        ),
                      ),
                    ],
                  ),
                ),
            
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
                          _buildSectionTitle(Icons.account_circle, 'Tài khoản đồng bộ'),
                          const SizedBox(height: 16),
                          if (_currentUser != null)
                            _buildUserCard()
                          else
                            _buildLoginCard(),
                          
                          const SizedBox(height: 48),

                          _buildSectionTitle(Icons.play_circle_outline, 'Trình phát video'),
                          const SizedBox(height: 16),
                          GlassContainer(
                            padding: const EdgeInsets.all(16),
                            child: SwitchListTile(
                              title: const Text('Tăng tốc phần cứng (GPU)'),
                              subtitle: const Text('Bật để xem mượt hơn. Tắt đi nếu xem phim bị lỗi hình ảnh hoặc văng ứng dụng.'),
                              value: _hwAccel,
                              activeColor: Colors.redAccent,
                              onChanged: (val) async {
                                final prefs = await SharedPreferences.getInstance();
                                await prefs.setBool('enable_hw_accel', val);
                                setState(() {
                                  _hwAccel = val;
                                });
                              },
                            ),
                          ),
                          
                          const SizedBox(height: 48),

                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              _buildSectionTitle(Icons.subtitles, L10n.t('subtitles')),
                              TextButton.icon(
                                onPressed: () async {
                                  final prefs = await SharedPreferences.getInstance();
                                  await prefs.setDouble('sub_size', 24.0);
                                  await prefs.setDouble('sub_opacity', 0.5);
                                  await prefs.setString('sub_color', 'White');
                                  await prefs.setString('sub_font', 'Roboto');
                                  setState(() {
                                    _subSize = 24.0;
                                    _subOpacity = 0.5;
                                    _subColor = 'White';
                                    _subFont = 'Roboto';
                                  });
                                },
                                icon: const Icon(Icons.restore, color: Colors.white70),
                                label: Text(L10n.t('restore_default'), style: const TextStyle(color: Colors.white70)),
                              ),
                            ],
                          ),
                          const SizedBox(height: 8),
                          Text(L10n.t('subtitle_note'), style: const TextStyle(color: Colors.white54, fontSize: 13, fontStyle: FontStyle.italic)),
                          const SizedBox(height: 16),
                          GlassContainer(
                            padding: const EdgeInsets.all(16),
                            child: Column(
                              children: [
                                // Khu vực xem trước phụ đề
                                Container(
                                  height: 120,
                                  width: double.infinity,
                                  decoration: BoxDecoration(
                                    color: Colors.black,
                                    borderRadius: BorderRadius.circular(12),
                                    image: const DecorationImage(
                                      image: AssetImage('assets/logo.png'), // Dùng tạm logo làm nền
                                      fit: BoxFit.cover,
                                      opacity: 0.3,
                                    ),
                                  ),
                                  alignment: Alignment.bottomCenter,
                                  padding: const EdgeInsets.only(bottom: 16),
                                  child: Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                    decoration: BoxDecoration(
                                      color: Colors.black.withOpacity(_subOpacity),
                                      borderRadius: BorderRadius.circular(4),
                                    ),
                                    child: Text(
                                      'Ví dụ: Phụ đề sẽ hiển thị như thế này.',
                                      style: TextStyle(
                                        color: _getColorFromName(_subColor),
                                        fontSize: _subSize,
                                        fontFamily: _subFont,
                                        fontWeight: FontWeight.bold,
                                        shadows: const [
                                          Shadow(offset: Offset(1, 1), blurRadius: 2, color: Colors.black),
                                          Shadow(offset: Offset(-1, -1), blurRadius: 2, color: Colors.black),
                                        ],
                                      ),
                                    ),
                                  ),
                                ),
                                const SizedBox(height: 24),
                                Row(
                                  children: [
                                    const SizedBox(width: 8),
                                    const Text('Kích thước chữ', style: TextStyle(color: Colors.white, fontSize: 16)),
                                    const SizedBox(width: 16),
                                    Expanded(
                                      child: Slider(
                                        value: _subSize,
                                        min: 16.0,
                                        max: 64.0,
                                        divisions: 24,
                                        label: _subSize.round().toString(),
                                        activeColor: Colors.amber,
                                        onChanged: (val) async {
                                          setState(() => _subSize = val);
                                          final prefs = await SharedPreferences.getInstance();
                                          await prefs.setDouble('sub_size', val);
                                        },
                                      ),
                                    ),
                                    SizedBox(
                                      width: 48,
                                      child: Text('${_subSize.round()} px', style: const TextStyle(color: Colors.white70)),
                                    ),
                                  ],
                                ),
                                const Divider(color: Colors.white12, height: 32),
                                Row(
                                  children: [
                                    const SizedBox(width: 8),
                                    const Text('Độ mờ nền chữ', style: TextStyle(color: Colors.white, fontSize: 16)),
                                    const SizedBox(width: 16),
                                    Expanded(
                                      child: Slider(
                                        value: _subOpacity,
                                        min: 0.0,
                                        max: 1.0,
                                        divisions: 20,
                                        label: '${(_subOpacity * 100).round()}%',
                                        activeColor: Colors.amber,
                                        onChanged: (val) async {
                                          setState(() => _subOpacity = val);
                                          final prefs = await SharedPreferences.getInstance();
                                          await prefs.setDouble('sub_opacity', val);
                                        },
                                      ),
                                    ),
                                    SizedBox(
                                      width: 48,
                                      child: Text('${(_subOpacity * 100).round()}%', style: const TextStyle(color: Colors.white70)),
                                    ),
                                  ],
                                ),
                                const Divider(color: Colors.white12, height: 32),
                                Row(
                                  children: [
                                    const SizedBox(width: 8),
                                    Text(L10n.t('sub_color'), style: const TextStyle(color: Colors.white, fontSize: 16)),
                                    const SizedBox(width: 16),
                                    DropdownButton<String>(
                                      value: _subColor,
                                      dropdownColor: Colors.black87,
                                      style: const TextStyle(color: Colors.amber, fontSize: 16),
                                      underline: const SizedBox(),
                                      items: [
                                        DropdownMenuItem(value: 'White', child: Text(L10n.t('color_white'))),
                                        DropdownMenuItem(value: 'Yellow', child: Text(L10n.t('color_yellow'))),
                                        DropdownMenuItem(value: 'Green', child: Text(L10n.t('color_green'))),
                                        DropdownMenuItem(value: 'Cyan', child: Text(L10n.t('color_cyan'))),
                                      ],
                                      onChanged: (val) async {
                                        if (val != null) {
                                          setState(() => _subColor = val);
                                          final prefs = await SharedPreferences.getInstance();
                                          await prefs.setString('sub_color', val);
                                        }
                                      },
                                    ),
                                  ],
                                ),
                                const Divider(color: Colors.white12, height: 32),
                                Row(
                                  children: [
                                    const SizedBox(width: 8),
                                    Text(L10n.t('sub_font'), style: const TextStyle(color: Colors.white, fontSize: 16)),
                                    const SizedBox(width: 16),
                                    DropdownButton<String>(
                                      value: _subFont,
                                      dropdownColor: Colors.black87,
                                      style: const TextStyle(color: Colors.amber, fontSize: 16),
                                      underline: const SizedBox(),
                                      items: [
                                        DropdownMenuItem(value: 'Roboto', child: Text(L10n.t('font_default'))),
                                        const DropdownMenuItem(value: 'Arial', child: Text('Arial')),
                                        const DropdownMenuItem(value: 'Times New Roman', child: Text('Times New Roman')),
                                        const DropdownMenuItem(value: 'Tahoma', child: Text('Tahoma')),
                                      ],
                                      onChanged: (val) async {
                                        if (val != null) {
                                          setState(() => _subFont = val);
                                          final prefs = await SharedPreferences.getInstance();
                                          await prefs.setString('sub_font', val);
                                        }
                                      },
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                          
                          const SizedBox(height: 48),

                          _buildSectionTitle(Icons.settings_suggest, L10n.t('health_utilities')),
                          const SizedBox(height: 16),
                          GlassContainer(
                            padding: const EdgeInsets.all(16),
                            child: Column(
                              children: [
                                SwitchListTile(
                                  title: Text(L10n.t('language'), style: const TextStyle(color: Colors.white, fontSize: 16)),
                                  subtitle: Text(_appLang == 'vi' ? 'Tiếng Việt' : 'English', style: const TextStyle(color: Colors.white70)),
                                  value: _appLang == 'vi',
                                  activeColor: Colors.amber,
                                  onChanged: (val) async {
                                    final newLang = val ? 'vi' : 'en';
                                    await L10n.load(newLang);
                                    setState(() {
                                      _appLang = newLang;
                                    });
                                  },
                                ),
                                const Divider(color: Colors.white12, height: 1),
                                SwitchListTile(
                                  title: Text(L10n.t('auto_next'), style: const TextStyle(color: Colors.white, fontSize: 16)),
                                  value: _autoNext,
                                  activeColor: Colors.amber,
                                  onChanged: (val) async {
                                    setState(() => _autoNext = val);
                                    final prefs = await SharedPreferences.getInstance();
                                    await prefs.setBool('auto_next', val);
                                  },
                                ),
                                const Divider(color: Colors.white12, height: 1),
                                SwitchListTile(
                                  title: Text(L10n.t('auto_play_trailer'), style: const TextStyle(color: Colors.white, fontSize: 16)),
                                  value: _autoPlayTrailer,
                                  activeColor: Colors.amber,
                                  onChanged: (val) async {
                                    setState(() => _autoPlayTrailer = val);
                                    final prefs = await SharedPreferences.getInstance();
                                    await prefs.setBool('auto_play_trailer', val);
                                  },
                                ),
                                const Divider(color: Colors.white12, height: 1),
                                ListTile(
                                  title: Text(L10n.t('default_speed'), style: const TextStyle(color: Colors.white, fontSize: 16)),
                                  trailing: DropdownButton<double>(
                                    value: _defaultSpeed,
                                    dropdownColor: Colors.black87,
                                    style: const TextStyle(color: Colors.amber, fontSize: 16),
                                    underline: const SizedBox(),
                                    items: const [
                                      DropdownMenuItem(value: 1.0, child: Text('1.0x')),
                                      DropdownMenuItem(value: 1.25, child: Text('1.25x')),
                                      DropdownMenuItem(value: 1.5, child: Text('1.5x')),
                                      DropdownMenuItem(value: 2.0, child: Text('2.0x')),
                                    ],
                                    onChanged: (val) async {
                                      if (val != null) {
                                        setState(() => _defaultSpeed = val);
                                        final prefs = await SharedPreferences.getInstance();
                                        await prefs.setDouble('default_speed', val);
                                      }
                                    },
                                  ),
                                ),
                                const Divider(color: Colors.white12, height: 1),
                                ListTile(
                                  title: Text(L10n.t('watch_limit'), style: const TextStyle(color: Colors.white, fontSize: 16)),
                                  trailing: DropdownButton<int>(
                                    value: _watchLimit,
                                    dropdownColor: Colors.black87,
                                    style: const TextStyle(color: Colors.amber, fontSize: 16),
                                    underline: const SizedBox(),
                                    items: [
                                      DropdownMenuItem(value: 0, child: Text(L10n.t('limit_off'))),
                                      DropdownMenuItem(value: 60, child: Text('60 ${L10n.t('limit_minutes')}')),
                                      DropdownMenuItem(value: 90, child: Text('90 ${L10n.t('limit_minutes')}')),
                                      DropdownMenuItem(value: 120, child: Text('120 ${L10n.t('limit_minutes')}')),
                                      DropdownMenuItem(value: 180, child: Text('180 ${L10n.t('limit_minutes')}')),
                                    ],
                                    onChanged: (val) async {
                                      if (val != null) {
                                        setState(() => _watchLimit = val);
                                        final prefs = await SharedPreferences.getInstance();
                                        await prefs.setInt('watch_limit', val);
                                      }
                                    },
                                  ),
                                ),
                              ],
                            ),
                          ),

                          const SizedBox(height: 48),
                          
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              _buildSectionTitle(Icons.source, 'Nguồn phim'),
                              TextButton.icon(
                                onPressed: () {
                                  bool allSelected = _sources.values.every((v) => v);
                                  setState(() {
                                    for (var key in _sources.keys) {
                                      _sources[key] = !allSelected;
                                    }
                                  });
                                  _saveSources();
                                },
                                icon: Icon(
                                  _sources.values.every((v) => v) ? Icons.deselect : Icons.select_all,
                                  color: Colors.white70,
                                ),
                                label: Text(
                                  _sources.values.every((v) => v) ? 'Bỏ chọn tất cả' : 'Chọn tất cả',
                                  style: const TextStyle(color: Colors.white70),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 8),
                          const Text(
                            'Chọn các nguồn phim bạn muốn sử dụng. Các nguồn bị tắt sẽ không xuất hiện khi tìm kiếm và duyệt phim.',
                            style: TextStyle(color: Colors.white54, fontSize: 14),
                          ),
                          const SizedBox(height: 24),
                          
                          // Nhóm Nguồn Promax
                          const Text(
                            'Nguồn Promax',
                            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.amber),
                          ),
                          const SizedBox(height: 12),
                          Wrap(
                            spacing: 16,
                            runSpacing: 16,
                            children: _sources.keys
                                .where((key) => key == 'premium' || key == 'torrentio')
                                .map((key) => _buildModernSourceCard(key))
                                .toList(),
                          ),
                          
                          const SizedBox(height: 24),
                          
                          // Nhóm Nguồn Standard
                          const Text(
                            'Nguồn Standard',
                            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.blueAccent),
                          ),
                          const SizedBox(height: 12),
                          Wrap(
                            spacing: 16,
                            runSpacing: 16,
                            children: _sources.keys
                                .where((key) => key != 'premium' && key != 'torrentio')
                                .map((key) => _buildModernSourceCard(key))
                                .toList(),
                          ),

                          const SizedBox(height: 48),

                          _buildSectionTitle(Icons.keyboard, 'Phím tắt'),
                          const SizedBox(height: 16),
                          GlassContainer(
                            padding: const EdgeInsets.all(20),
                            child: Column(
                              children: [
                                _buildShortcutRow('F11', 'Phóng to / Thu nhỏ toàn màn hình (Full Screen)'),
                                const Divider(color: Colors.white12, height: 32),
                                _buildShortcutRow('ESC', 'Thoát / Đóng hộp thoại'),
                                const Divider(color: Colors.white12, height: 32),
                                _buildShortcutRow('Space (Cách)', 'Tạm dừng / Phát video'),
                                const Divider(color: Colors.white12, height: 32),
                                _buildShortcutRow('F', 'Phóng to video (khi đang xem)'),
                                const Divider(color: Colors.white12, height: 32),
                                _buildShortcutRow('Mũi tên Trái / Phải', 'Tua video 10 giây'),
                              ],
                            ),
                          ),

                          const SizedBox(height: 48),

                          _buildSectionTitle(Icons.info_outline, 'Thông tin & Liên hệ'),
                          const SizedBox(height: 16),
                          _buildAppInfoCard(),
                          
                          const SizedBox(height: 64), // Extra bottom padding
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
      const Positioned(
        top: 0, left: 0, right: 0,
        child: CustomTitleBar(),
      ),
    ],
  ),
);
}

  Widget _buildSectionTitle(IconData icon, String title) {
    return Row(
      children: [
        Icon(icon, color: Colors.blueAccent, size: 24),
        const SizedBox(width: 12),
        Text(
          title,
          style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white),
        ),
      ],
    );
  }

  Widget _buildUserCard() {
    return GlassContainer(
      padding: const EdgeInsets.all(20),
      borderRadius: 16,
      child: Row(
        children: [
          CircleAvatar(
            radius: 36,
            backgroundImage: _currentUser!['photoURL']!.isNotEmpty 
                ? CachedNetworkImageProvider(_currentUser!['photoURL']!) 
                : null,
            child: _currentUser!['photoURL']!.isEmpty ? const Icon(Icons.person, size: 36) : null,
          ),
          const SizedBox(width: 20),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  _currentUser!['displayName']!,
                  style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white),
                ),
                const SizedBox(height: 6),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.green.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.green.withOpacity(0.5)),
                  ),
                  child: const Text('Đã đồng bộ với TV4U Web', style: TextStyle(color: Colors.greenAccent, fontSize: 12, fontWeight: FontWeight.bold)),
                ),
              ],
            ),
          ),
          OutlinedButton.icon(
            onPressed: _handleLogout,
            icon: const Icon(Icons.logout, size: 18),
            label: const Text('Đăng xuất'),
            style: OutlinedButton.styleFrom(
              foregroundColor: Colors.redAccent,
              side: const BorderSide(color: Colors.redAccent),
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLoginCard() {
    return GlassContainer(
      padding: const EdgeInsets.all(32),
      borderRadius: 16,
      child: Column(
        children: [
          const Icon(Icons.cloud_sync, size: 48, color: Colors.white54),
          const SizedBox(height: 16),
          const Text(
            'Đăng nhập để đồng bộ lịch sử xem phim và danh sách yêu thích của bạn giữa phiên bản Web và Ứng dụng Desktop.',
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.white70, fontSize: 15),
          ),
          const SizedBox(height: 24),
          ElevatedButton.icon(
            icon: _isLoggingIn 
                ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.black, strokeWidth: 2)) 
                : const Icon(Icons.login),
            label: Text(_isLoggingIn ? 'Đang mở trình duyệt...' : 'Đăng nhập với Google'),
            onPressed: _isLoggingIn ? null : _handleLogin,
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.white,
              foregroundColor: Colors.black,
              padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
              textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              elevation: 4,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildModernSourceCard(String sourceKey) {
    String sourceName = sourceKey.toUpperCase();
    if (sourceKey == 'nguonc') sourceName = 'NguonC';
    if (sourceKey == 'ophim') sourceName = 'Ophim';
    if (sourceKey == 'kkphim') sourceName = 'KKPhim';
    if (sourceKey == 'vsmov') sourceName = 'VSMov';
    if (sourceKey == 'phim4k') sourceName = 'Phim4K';
    if (sourceKey == 'free1') sourceName = 'Free1';
    if (sourceKey == 'motchill') sourceName = 'Motchill';
    if (sourceKey == 'torrentio') sourceName = 'Torrent (P2P)';
    
    final bool isEnabled = _sources[sourceKey] ?? true;
    
    return InkWell(
      onTap: () {
        setState(() {
          _sources[sourceKey] = !isEnabled;
        });
        _saveSources();
      },
      borderRadius: BorderRadius.circular(12),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        width: 240,
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: isEnabled ? Colors.white.withOpacity(0.08) : Colors.white.withOpacity(0.02),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isEnabled ? Colors.blueAccent.withOpacity(0.5) : Colors.white.withOpacity(0.1),
            width: isEnabled ? 2 : 1,
          ),
          boxShadow: isEnabled ? [
            BoxShadow(
              color: Colors.blueAccent.withOpacity(0.1),
              blurRadius: 8,
              spreadRadius: 0,
            )
          ] : [],
        ),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: isEnabled ? Colors.blueAccent.withOpacity(0.2) : Colors.white.withOpacity(0.1),
                shape: BoxShape.circle,
              ),
              child: Icon(
                Icons.dns,
                color: isEnabled ? Colors.blueAccent : Colors.white54,
                size: 20,
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Text(
                sourceName,
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: isEnabled ? Colors.white : Colors.white54,
                ),
              ),
            ),
            Switch(
              value: isEnabled,
              activeColor: Colors.blueAccent,
              onChanged: (val) {
                setState(() {
                  _sources[sourceKey] = val;
                });
                _saveSources();
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAppInfoCard() {
    if (_isLoadingAppInfo) {
      return const GlassContainer(
        padding: EdgeInsets.all(32),
        borderRadius: 16,
        child: Center(child: CircularProgressIndicator()),
      );
    }
    
    return GlassContainer(
      padding: const EdgeInsets.all(24),
      borderRadius: 16,
      child: Column(
        children: [
          Image.asset('assets/logo.png', height: 48),
          const SizedBox(height: 24),
          _buildInfoRow('Phiên bản', UpdateApi.currentAppVersion),
          const SizedBox(height: 16),
          Align(
            alignment: Alignment.centerRight,
            child: Wrap(
              spacing: 12,
              runSpacing: 12,
              alignment: WrapAlignment.end,
              children: [
                if (UpdateApi.currentAppVersion.contains('.beta'))
                  OutlinedButton.icon(
                    onPressed: () async {
                      showDialog(
                        context: context,
                        barrierDismissible: false,
                        builder: (_) => const Center(child: CircularProgressIndicator()),
                      );
                      
                      final publicInfo = await UpdateApi.getPublicUpdateInfo();
                      
                      if (mounted) {
                        Navigator.of(context).pop();
                        
                        if (publicInfo != null) {
                          showDialog(
                            context: context,
                            builder: (context) => UpdateDialog(updateInfo: publicInfo),
                          );
                        } else {
                          UIUtils.showCustomSnackBar(context, 'Không tìm thấy bản Public!');
                        }
                      }
                    },
                    icon: const Icon(Icons.download, size: 16, color: Colors.blueAccent),
                    label: const Text('Trở về bản Public', style: TextStyle(color: Colors.blueAccent)),
                    style: OutlinedButton.styleFrom(
                      side: const BorderSide(color: Colors.blueAccent),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                    ),
                  ),
                OutlinedButton.icon(
                  onPressed: () async {
                    // Hiển thị dialog đang tải
                    showDialog(
                      context: context,
                      barrierDismissible: false,
                      builder: (_) => const Center(child: CircularProgressIndicator()),
                    );
                    
                    final updateInfo = await UpdateApi.checkForUpdate();
                    
                    if (mounted) {
                      Navigator.of(context).pop(); // Đóng loading
                      
                      if (updateInfo != null) {
                        showDialog(
                          context: context,
                          barrierDismissible: !updateInfo.isForceUpdate,
                          builder: (context) => UpdateDialog(updateInfo: updateInfo),
                        );
                      } else {
                        UIUtils.showCustomSnackBar(context, 'Bạn đang sử dụng phiên bản mới nhất!');
                      }
                    }
                  },
                  icon: const Icon(Icons.system_update, size: 16, color: Colors.amber),
                  label: const Text('Kiểm tra phiên bản mới', style: TextStyle(color: Colors.amber)),
                  style: OutlinedButton.styleFrom(
                    side: const BorderSide(color: Colors.amber),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                  ),
                ),
              ],
            ),
          ),
          const Divider(color: Colors.white12, height: 32),
          _buildInfoRow('Nhà phát triển', _appSettings?['developer'] ?? 'Sparky'),
          const Divider(color: Colors.white12, height: 32),
          _buildInfoRow('Liên hệ', _appSettings?['contact'] ?? 'mytv4u.web.app'),
          if (_appSettings != null && _appSettings!['facebook'] != null && _appSettings!['facebook'].toString().isNotEmpty) ...[
            const Divider(color: Colors.white12, height: 32),
            _buildInfoRow('Facebook', _appSettings!['facebook']),
          ],
          const Divider(color: Colors.white12, height: 32),
          SizedBox(
            width: double.infinity,
            child: OutlinedButton.icon(
              onPressed: _showTermsDialog,
              icon: const Icon(Icons.gavel, color: Colors.blueAccent, size: 18),
              label: const Text('Điều khoản sử dụng & Miễn trừ trách nhiệm', style: TextStyle(color: Colors.blueAccent)),
              style: OutlinedButton.styleFrom(
                side: const BorderSide(color: Colors.blueAccent),
                padding: const EdgeInsets.symmetric(vertical: 14),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _showTermsDialog() {
    showGeneralDialog(
      context: context,
      barrierDismissible: true,
      barrierLabel: 'Dismiss',
      barrierColor: Colors.black.withOpacity(0.5),
      transitionDuration: const Duration(milliseconds: 300),
      pageBuilder: (context, anim1, anim2) {
        return Align(
          alignment: Alignment.center,
          child: Material(
            color: Colors.transparent,
            child: ClipRRect(
              borderRadius: BorderRadius.circular(24),
              child: BackdropFilter(
                filter: ImageFilter.blur(sigmaX: 20, sigmaY: 20),
                child: Container(
                  width: 650,
                  constraints: BoxConstraints(maxHeight: MediaQuery.of(context).size.height * 0.85),
                  decoration: BoxDecoration(
                    color: const Color(0xFF141416).withOpacity(0.65),
                    borderRadius: BorderRadius.circular(24),
                    border: Border.all(color: Colors.white.withOpacity(0.1)),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.4),
                        blurRadius: 32,
                        offset: const Offset(0, 16),
                      )
                    ],
                  ),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      // Header
                      Container(
                        padding: const EdgeInsets.all(24),
                        decoration: BoxDecoration(
                          border: Border(bottom: BorderSide(color: Colors.white.withOpacity(0.05))),
                        ),
                        child: Row(
                          children: [
                            Container(
                              padding: const EdgeInsets.all(8),
                              decoration: BoxDecoration(
                                color: Colors.blueAccent.withOpacity(0.1),
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: const Icon(Icons.shield, color: Colors.blueAccent),
                            ),
                            const SizedBox(width: 16),
                            const Expanded(
                              child: Text(
                                'Điều Khoản Sử Dụng & DMCA',
                                style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),
                              ),
                            ),
                            IconButton(
                              icon: const Icon(Icons.close, color: Colors.white54),
                              onPressed: () => Navigator.pop(context),
                              hoverColor: Colors.white.withOpacity(0.1),
                              splashRadius: 24,
                            ),
                          ],
                        ),
                      ),
                      
                      // Body
                      Flexible(
                        child: SingleChildScrollView(
                          padding: const EdgeInsets.all(32),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              _buildTermSection(
                                icon: Icons.storage,
                                iconColor: Colors.blueAccent,
                                title: '1. Tổng Hợp Nguồn & Bản Quyền',
                                content: 'MyTV4U là công cụ tự động tìm kiếm và tổng hợp liên kết phát trực tuyến công khai. Ứng dụng TUYỆT ĐỐI KHÔNG sở hữu, KHÔNG lưu trữ (host), KHÔNG tải lên và KHÔNG phân phối bất kỳ tệp tin phương tiện nào. Tất cả nội dung số hiển thị trên MyTV4U đều được truyền tải trực tiếp từ các máy chủ bên thứ ba độc lập.',
                              ),
                              const SizedBox(height: 32),
                              _buildTermSection(
                                icon: Icons.warning_amber_rounded,
                                iconColor: Colors.amber,
                                title: '2. Tính Khả Dụng Của Nguồn',
                                content: 'Các nguồn phát trực tuyến (M3U8) phụ thuộc 100% vào máy chủ bên ngoài (NguonC, KKPhim, TV360, VSMov...). Chúng có thể bị gián đoạn, đổi cấu hình hoặc ngừng hoạt động vĩnh viễn bất kỳ lúc nào bởi quyết định của máy chủ bên thứ ba. Đội ngũ phát triển MyTV4U không có thẩm quyền can thiệp hay đảm bảo tính ổn định.',
                              ),
                              const SizedBox(height: 32),
                              _buildTermSection(
                                icon: Icons.developer_mode,
                                iconColor: Colors.greenAccent,
                                title: '3. Phạm Vi Phát Triển',
                                content: 'MyTV4U định vị là một công cụ phần mềm. Đội ngũ phát triển chỉ nghiên cứu và xây dựng UI/UX đồng bộ đa nền tảng, thuật toán tìm kiếm, framework ứng dụng, custom video player engine, và hệ thống đồng bộ lịch sử xem.',
                              ),
                              const SizedBox(height: 32),
                              _buildTermSection(
                                icon: Icons.gavel,
                                iconColor: Colors.pinkAccent,
                                title: '4. Yêu Cầu Gỡ Bỏ (DMCA)',
                                content: 'Người dùng tự chịu trách nhiệm đối với hành vi truy cập. Nếu bạn là chủ sở hữu bản quyền, vui lòng gửi yêu cầu gỡ bỏ trực tiếp (DMCA Takedown) đến đơn vị quản lý máy chủ lưu trữ (Host Provider) của bên thứ ba đang trực tiếp chứa tệp tin đó.',
                              ),
                            ],
                          ),
                        ),
                      ),
                      
                      // Footer
                      Container(
                        padding: const EdgeInsets.all(24),
                        decoration: BoxDecoration(
                          border: Border(top: BorderSide(color: Colors.white.withOpacity(0.05))),
                          color: Colors.white.withOpacity(0.02),
                          borderRadius: const BorderRadius.only(bottomLeft: Radius.circular(24), bottomRight: Radius.circular(24)),
                        ),
                        child: ElevatedButton(
                          onPressed: () => Navigator.pop(context),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.white,
                            foregroundColor: Colors.black,
                            padding: const EdgeInsets.symmetric(vertical: 18),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                            elevation: 0,
                          ),
                          child: const Text('Tôi đã hiểu & Đồng ý', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        );
      },
      transitionBuilder: (context, anim1, anim2, child) {
        return FadeTransition(
          opacity: anim1,
          child: ScaleTransition(
            scale: Tween<double>(begin: 0.95, end: 1.0).animate(CurvedAnimation(parent: anim1, curve: Curves.easeOutCubic)),
            child: child,
          ),
        );
      },
    );
  }

  Widget _buildShortcutRow(String keyName, String action) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(action, style: const TextStyle(color: Colors.white, fontSize: 15)),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.1),
            borderRadius: BorderRadius.circular(6),
            border: Border.all(color: Colors.white24),
          ),
          child: Text(
            keyName,
            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13, fontFamily: 'monospace'),
          ),
        ),
      ],
    );
  }

  Widget _buildTermSection({required IconData icon, required Color iconColor, required String title, required String content}) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: iconColor.withOpacity(0.1),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Icon(icon, color: iconColor, size: 24),
        ),
        const SizedBox(width: 20),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 12),
              Text(
                content,
                style: const TextStyle(color: Colors.white70, fontSize: 14, height: 1.7),
              ),
            ],
          ),
        ),
      ],
    );
  }
  
  Widget _buildInfoRow(String label, String value) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(label, style: const TextStyle(color: Colors.white54, fontSize: 16)),
        Text(value, style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.w600)),
      ],
    );
  }
}

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../widgets/glass_container.dart';
import '../widgets/custom_title_bar.dart';
import '../utils/l10n.dart';
import '../utils/ui_utils.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({Key? key}) : super(key: key);

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool _hwAccel = true;
  double _subSize = 24.0;
  double _subOpacity = 0.3;
  String _subColor = 'White';
  String _subFont = 'Roboto';
  bool _autoNext = true;
  bool _autoPlayTrailer = true;
  double _defaultSpeed = 1.0;
  String _appLang = 'vi';

  @override
  void initState() {
    super.initState();
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    
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
        _appLang = prefs.getString('app_lang') ?? 'vi';
      });
    }
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: Text(L10n.t('settings'), style: const TextStyle(color: Colors.white)),
        backgroundColor: Colors.transparent,
        elevation: 0,
        iconTheme: const IconThemeData(color: Colors.white),
      ),
      extendBodyBehindAppBar: true,
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(24),
          children: [
            _buildSectionTitle(Icons.language, L10n.t('language_settings')),
            const SizedBox(height: 16),
            GlassContainer(
              padding: const EdgeInsets.all(16),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(L10n.t('language'), style: const TextStyle(color: Colors.white, fontSize: 16)),
                  DropdownButton<String>(
                    value: _appLang,
                    dropdownColor: Colors.black87,
                    style: const TextStyle(color: Colors.amber, fontSize: 16),
                    underline: const SizedBox(),
                    items: [
                      DropdownMenuItem(value: 'vi', child: Text(L10n.t('lang_vi'))),
                      DropdownMenuItem(value: 'en', child: Text('English')),
                    ],
                    onChanged: (val) async {
                      if (val != null) {
                        await L10n.load(val);
                        setState(() {
                          _appLang = val;
                        });
                        final prefs = await SharedPreferences.getInstance();
                        prefs.setString('app_lang', val);
                      }
                    },
                  ),
                ],
              ),
            ),
            
            const SizedBox(height: 32),
            _buildSectionTitle(Icons.play_circle_outline, L10n.t('video_player')),
            const SizedBox(height: 16),
            GlassContainer(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  SwitchListTile(
                    title: Text(L10n.t('hw_accel'), style: const TextStyle(color: Colors.white)),
                    subtitle: Text(L10n.t('hw_accel_desc'), style: const TextStyle(color: Colors.white54)),
                    value: _hwAccel,
                    activeColor: Colors.redAccent,
                    onChanged: (val) async {
                      setState(() => _hwAccel = val);
                      final prefs = await SharedPreferences.getInstance();
                      await prefs.setBool('enable_hw_accel', val);
                    },
                  ),
                  const Divider(color: Colors.white12),
                  SwitchListTile(
                    title: Text(L10n.t('auto_next'), style: const TextStyle(color: Colors.white)),
                    value: _autoNext,
                    activeColor: Colors.amber,
                    onChanged: (val) async {
                      setState(() => _autoNext = val);
                      final prefs = await SharedPreferences.getInstance();
                      await prefs.setBool('auto_next', val);
                    },
                  ),
                ],
              ),
            ),
            const SizedBox(height: 32),
            _buildSectionTitle(Icons.info, L10n.t('info_contact')),
            const SizedBox(height: 16),
            const GlassContainer(
              padding: EdgeInsets.all(16),
              child: ListTile(
                title: Text('MyTV4U Core', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                subtitle: Text('Version 2.0 (Addon Engine)', style: TextStyle(color: Colors.white70)),
              ),
            )
          ],
        ),
      ),
    );
  }
}

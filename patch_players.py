import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add import
    if "hardware_info.dart" not in content:
        content = content.replace("import '../models/movie.dart';", "import '../utils/hardware_info.dart';\nimport '../models/movie.dart';")

    # Add _systemRamMB state
    if "_systemRamMB" not in content:
        content = content.replace("bool _isPlayerInitialized = false;", "bool _isPlayerInitialized = false;\n  int _systemRamMB = 4096;")
        # For tv_player_screen
        content = content.replace("bool _isPlayerInit = false;", "bool _isPlayerInit = false;\n  int _systemRamMB = 4096;")

    # Add await HardwareInfo in _loadSettingsAndInit
    load_settings_block = '''    final prefs = await SharedPreferences.getInstance();
    if (mounted) {
      setState(() {
        _hwAccel = prefs.getBool('enable_hw_accel') ?? true;'''
        
    new_load_settings = '''    final prefs = await SharedPreferences.getInstance();
    _systemRamMB = await HardwareInfo.getSystemRamMB();
    if (mounted) {
      setState(() {
        _hwAccel = prefs.getBool('enable_hw_accel') ?? true;'''
    
    content = content.replace(load_settings_block, new_load_settings)
    
    # Replace _initMediaKit
    old_init = '''  void _initMediaKit() {
    player = Player(
      configuration: const PlayerConfiguration(
        bufferSize: 32 * 1024 * 1024,
        pitch: false,
      ),
    );'''

    new_init = '''  void _initMediaKit() {
    int bufferSize = 32 * 1024 * 1024;
    String demuxerMaxBytes = '64M';
    String demuxerMaxBackBytes = '32M';
    
    if (_systemRamMB > 8192) {
      bufferSize = 128 * 1024 * 1024;
      demuxerMaxBytes = '256M';
      demuxerMaxBackBytes = '128M';
    } else if (_systemRamMB > 4096) {
      bufferSize = 64 * 1024 * 1024;
      demuxerMaxBytes = '128M';
      demuxerMaxBackBytes = '64M';
    }

    player = Player(
      configuration: PlayerConfiguration(
        bufferSize: bufferSize,
        pitch: false,
      ),
    );'''

    content = content.replace(old_init, new_init)
    
    # Update setProperty calls
    old_props = '''      platform.setProperty('cache', 'yes');
      platform.setProperty('cache-pause', 'no'); // Phát ngay khi có dữ liệu, không chờ đầy buffer
      platform.setProperty('demuxer-max-bytes', '64M');
      platform.setProperty('demuxer-max-back-bytes', '32M');'''
      
    new_props = '''      platform.setProperty('cache', 'yes');
      platform.setProperty('cache-pause', 'no');
      platform.setProperty('demuxer-max-bytes', demuxerMaxBytes);
      platform.setProperty('demuxer-max-back-bytes', demuxerMaxBackBytes);
      
      // Tối ưu 8K / HLS
      platform.setProperty('vd-lavc-threads', '16'); // Huy động CPU đa luồng
      platform.setProperty('vo', 'gpu-next'); // Engine render thế hệ mới (nét & mượt hơn)
      platform.setProperty('framedrop', 'decoder'); // Cho phép rớt frame để chống đứng máy khi tải quá nặng'''

    content = content.replace(old_props, new_props)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_file('lib/screens/player_screen.dart')
patch_file('lib/screens/tv_player_screen.dart')
print("Patched both player screens!")

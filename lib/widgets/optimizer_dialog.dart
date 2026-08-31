import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../utils/optimizer_utils.dart';
import '../utils/l10n.dart';
import '../globals.dart';
import 'ambient_background.dart';
import 'glass_container.dart';

class OptimizerDialog extends StatefulWidget {
  const OptimizerDialog({super.key});

  @override
  State<OptimizerDialog> createState() => _OptimizerDialogState();
}

class _OptimizerDialogState extends State<OptimizerDialog> {
  bool _isScanning = true;
  OptimizerResult? _result;

  bool _recMinimalist = false;
  bool _recDisableAmbient = false;
  bool _recDisableTrailer = false;
  bool _recDisableAudioEffects = false;
  bool _recAllEffects = false;

  Map<String, dynamic> _backupSettings = {};

  @override
  void initState() {
    super.initState();
    _scanSystem();
  }

  Future<void> _scanSystem() async {
    final ram = await OptimizerUtils.getRamMB();
    final cpu = await OptimizerUtils.getCpuName();
    final gpu = await OptimizerUtils.getGpuName();
    final isBattery = await OptimizerUtils.isOnBattery();
    final speed = await OptimizerUtils.testNetworkSpeed();
    
    final size = await OptimizerUtils.getScreenResolution(); 

    if (mounted) {
      setState(() {
        _result = OptimizerResult(
          ramMB: ram,
          cpuName: cpu,
          gpuName: gpu,
          isBattery: isBattery,
          networkMbps: speed,
          resolution: size,
        );
        _generateRecommendations();
        _isScanning = false;
      });
    }
  }

  void _generateRecommendations() {
    if (_result!.isLowEnd) {
      _recMinimalist = true;
      _recDisableAmbient = true;
      _recDisableTrailer = true;
      _recDisableAudioEffects = true;
    } else {
      if (_result!.isBattery) {
        _recDisableAmbient = true;
        _recDisableTrailer = true;
        _recDisableAudioEffects = true;
      }
      
      bool isNetworkSlow = _result!.networkMbps > 0 && _result!.networkMbps < 15.0;
      if (isNetworkSlow) {
        _recDisableTrailer = true;
      }

      if (_result!.isHighEnd && !_result!.isBattery && !isNetworkSlow) {
        _recAllEffects = true;
      }
    }
  }

  Future<void> _applyOptimization() async {
    final prefs = await SharedPreferences.getInstance();
    
    // Save current settings to backup before applying
    _backupSettings = {
      'minimalist_ui': prefs.getBool('minimalist_ui') ?? false,
      'enable_ambient_bg': prefs.getBool('enable_ambient_bg') ?? true,
      'auto_play_trailer': prefs.getBool('auto_play_trailer') ?? true,
      'enable_easter_eggs': prefs.getBool('enable_easter_eggs') ?? true,
      'audio_visualizer': prefs.getString('audio_visualizer') ?? 'bars',
      'audio_vinyl': prefs.getBool('audio_vinyl') ?? true,
    };
    
    await prefs.setString('optimizer_backup', jsonEncode(_backupSettings));

    if (_recMinimalist) {
      await prefs.setBool('minimalist_ui', true);
      isMinimalistUi.value = true;
    }
    if (_recDisableAmbient) {
      await prefs.setBool('enable_ambient_bg', false);
      globalEnableAmbient.value = false;
    }
    if (_recDisableTrailer) {
      await prefs.setBool('auto_play_trailer', false);
    }
    if (_recDisableAudioEffects) {
      await prefs.setString('audio_visualizer', 'none');
      await prefs.setBool('audio_vinyl', false);
    }
    if (_recAllEffects) {
      await prefs.setBool('minimalist_ui', false);
      isMinimalistUi.value = false;
      await prefs.setBool('enable_ambient_bg', true);
      globalEnableAmbient.value = true;
      await prefs.setBool('enable_easter_eggs', true);
      await prefs.setString('audio_visualizer', 'bars');
      await prefs.setBool('audio_vinyl', true);
    }

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(L10n.t('opt_msg_apply') ?? 'Đã áp dụng tối ưu giao diện! Các khuyến cáo video vui lòng tự điều chỉnh.'),
          backgroundColor: Colors.blueAccent,
        ),
      );
      Navigator.of(context).pop(_backupSettings); 
    }
  }

  Future<void> _undoOptimization() async {
    final prefs = await SharedPreferences.getInstance();
    final backupStr = prefs.getString('optimizer_backup');
    if (backupStr != null) {
      final Map<String, dynamic> backup = jsonDecode(backupStr);
      await prefs.setBool('minimalist_ui', backup['minimalist_ui'] ?? false);
      isMinimalistUi.value = backup['minimalist_ui'] ?? false;
      
      await prefs.setBool('enable_ambient_bg', backup['enable_ambient_bg'] ?? true);
      globalEnableAmbient.value = backup['enable_ambient_bg'] ?? true;
      
      await prefs.setBool('auto_play_trailer', backup['auto_play_trailer'] ?? true);
      await prefs.setBool('enable_easter_eggs', backup['enable_easter_eggs'] ?? true);
      
      if (backup.containsKey('audio_visualizer')) {
        await prefs.setString('audio_visualizer', backup['audio_visualizer']);
      }
      if (backup.containsKey('audio_vinyl')) {
        await prefs.setBool('audio_vinyl', backup['audio_vinyl']);
      }
      await prefs.setString('audio_visualizer', backup['audio_visualizer'] ?? 'bars');
      await prefs.setBool('audio_vinyl', backup['audio_vinyl'] ?? true);
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(L10n.t('opt_msg_undo') ?? 'Đã khôi phục cài đặt trước khi tối ưu!'), backgroundColor: Colors.green),
        );
        Navigator.of(context).pop(true); // Return true to trigger UI refresh
      }
    } else {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(L10n.t('opt_msg_noundo') ?? 'Không tìm thấy bản sao lưu nào!'), backgroundColor: Colors.redAccent),
        );
      }
    }
  }

  Future<void> _resetToDefault() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('minimalist_ui', false);
    isMinimalistUi.value = false;
    await prefs.setBool('enable_ambient_bg', true);
    globalEnableAmbient.value = true;
    await prefs.setBool('auto_play_trailer', true);
    await prefs.setBool('enable_easter_eggs', true);
    await prefs.setString('audio_visualizer', 'bars');
    await prefs.setBool('audio_vinyl', true);
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(L10n.t('opt_msg_default') ?? 'Đã khôi phục cài đặt gốc của Tối ưu hoá!')),
      );
      Navigator.of(context).pop(true);
    }
  }

  Widget _buildRichLine(IconData icon, Color iconColor, String boldText, String normalText) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: iconColor, size: 24),
          const SizedBox(width: 12),
          Expanded(
            child: RichText(
              text: TextSpan(
                style: const TextStyle(fontSize: 15, color: Colors.white, height: 1.4),
                children: [
                  TextSpan(text: boldText, style: const TextStyle(fontWeight: FontWeight.bold)),
                  TextSpan(text: normalText, style: const TextStyle(color: Colors.white70)),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  List<Widget> _buildConversationalRecommendation() {
    List<Widget> widgets = [];
    
    if (_result!.isHighEnd) {
       widgets.add(_buildRichLine(Icons.rocket_launch, Colors.greenAccent, 
         L10n.t('opt_high_end_title') ?? "Tuyệt vời! ", 
         L10n.t('opt_high_end_desc') ?? "Cấu hình của bạn đủ sức chơi video 4K, thoải mái bật các thiết lập đồ họa đẹp nhất của ứng dụng."));
    } else if (_result!.isLowEnd) {
       widgets.add(_buildRichLine(Icons.warning_amber, Colors.amber, 
         L10n.t('opt_low_end_title') ?? "Cấu hình khiêm tốn: ", 
         L10n.t('opt_low_end_desc') ?? "Hệ thống sẽ đề xuất tự động tắt hiệu ứng kính mờ và các hiệu ứng sóng âm nhạc đồ hoạ nặng để trải nghiệm của bạn mượt mà nhất."));
    } else {
       widgets.add(_buildRichLine(Icons.check_circle, Colors.blueAccent, 
         L10n.t('opt_std_title') ?? "Cấu hình tiêu chuẩn: ", 
         L10n.t('opt_std_desc') ?? "Máy tính của bạn hoàn toàn đáp ứng tốt để trải nghiệm video ở mức 1080p."));
    }

    if (_result!.isBattery) {
       widgets.add(_buildRichLine(Icons.battery_alert, Colors.orangeAccent, 
         L10n.t('opt_bat_title') ?? "Đang dùng Pin: ", 
         L10n.t('opt_bat_desc') ?? "Nếu bạn muốn cày phim lâu hơn, hãy ưu tiên chọn chất lượng 1080p và đồng ý tắt bớt hiệu ứng nền (nếu có). Ngoài ra, khi nghe nhạc, hãy tắt hiệu ứng Sóng âm và Đĩa than để tiết kiệm điện tối đa."));
    } else if (_result!.resolution.height <= 1080) {
       widgets.add(_buildRichLine(Icons.monitor, Colors.white70, 
         L10n.t('opt_fhd_title') ?? "Màn hình Full HD: ", 
         L10n.t('opt_fhd_desc') ?? "Màn hình hiện tại không hiển thị được 4K, do đó bạn chỉ nên chọn video 1080p để tránh hao phí CPU vô ích."));
    }

    if (_result!.networkMbps > 0 && _result!.networkMbps < 15.0) {
       widgets.add(_buildRichLine(Icons.wifi_tethering_error, Colors.redAccent, 
         (L10n.t('opt_net_title') ?? "Mạng khá chậm") + " (${_result!.networkMbps.toStringAsFixed(1)} Mbps): ", 
         L10n.t('opt_net_desc') ?? "Bạn nên đổi mức chất lượng phát video mặc định về 720p hoặc 1080p để xem phim không bị gián đoạn."));
    }
    
    return widgets;
  }

  Widget _buildSpecChip(IconData icon, String title, String value) {
    return Container(
      width: 145, // Slightly wider to fit English and 13th Gen better
      padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 12),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.05),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.white12, width: 1),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: Colors.blueAccent, size: 16),
              const SizedBox(width: 8),
              Expanded(child: Text(title, style: const TextStyle(color: Colors.white54, fontSize: 12), maxLines: 1, overflow: TextOverflow.ellipsis)),
            ],
          ),
          const SizedBox(height: 6),
          Text(value, style: const TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold), maxLines: 2, overflow: TextOverflow.ellipsis),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: Colors.transparent,
      insetPadding: const EdgeInsets.all(24),
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 800, maxHeight: 750),
        child: GlassContainer(
          padding: const EdgeInsets.all(32),
          child: _isScanning ? _buildScanningState() : _buildResultState(),
        ),
      ),
    );
  }

  Widget _buildScanningState() {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 60.0),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const CircularProgressIndicator(color: Colors.blueAccent),
          const SizedBox(height: 24),
          Text(L10n.t('optimizer_scanning') ?? 'Đang quét hệ thống...', style: const TextStyle(color: Colors.white, fontSize: 18)),
          const SizedBox(height: 12),
          Text(L10n.t('opt_scan_sub') ?? 'Kiểm tra Chip, RAM, Màn hình, Pin và Tốc độ mạng...', style: const TextStyle(color: Colors.white54, fontSize: 14)),
        ],
      ),
    );
  }

  Widget _buildResultState() {
    final res = _result!;
    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            const Icon(Icons.rocket_launch, color: Colors.blueAccent, size: 32),
            const SizedBox(width: 16),
            Text(L10n.t('smart_optimizer') ?? 'Trợ lý Tối ưu hoá', style: const TextStyle(color: Colors.white, fontSize: 26, fontWeight: FontWeight.bold)),
          ],
        ),
        const SizedBox(height: 24),
        
        // Cấu hình (Specs)
        Wrap(
          spacing: 12,
          runSpacing: 12,
          children: [
            _buildSpecChip(Icons.memory, L10n.t('opt_spec_cpu') ?? "CPU", res.cpuName),
            _buildSpecChip(Icons.developer_board, L10n.t('opt_spec_gpu') ?? "GPU", res.gpuName),
            _buildSpecChip(Icons.sd_storage, L10n.t('opt_spec_ram') ?? "RAM", "${res.ramMB} MB"),
            _buildSpecChip(Icons.desktop_windows, L10n.t('opt_spec_screen') ?? "Màn hình", "${res.resolution.width.toInt()}x${res.resolution.height.toInt()} ${res.isBattery ? '(Pin)' : '(AC)'}"),
            _buildSpecChip(Icons.network_check, L10n.t('opt_spec_net') ?? "Tốc độ mạng", res.networkMbps > 0 ? "${res.networkMbps.toStringAsFixed(1)} Mbps" : (L10n.t('opt_net_err') ?? "Lỗi đo mạng")),
          ],
        ),

        const SizedBox(height: 32),
        
        // Khuyến cáo
        Text('💡 ${L10n.t('opt_specs') ?? 'Khuyến cáo thông minh:'}', style: const TextStyle(color: Colors.amber, fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 16),
        Flexible(
          child: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                ..._buildConversationalRecommendation(),
                const SizedBox(height: 16),
                const Divider(color: Colors.white12),
                const SizedBox(height: 16),
                Text(L10n.t('opt_apply_title') ?? 'Tự động áp dụng cài đặt giao diện (Tích chọn nếu muốn):', style: const TextStyle(color: Colors.white70, fontSize: 14, fontWeight: FontWeight.bold)),
                const SizedBox(height: 8),
                CheckboxListTile(
                  contentPadding: EdgeInsets.zero,
                  title: Text(L10n.t('opt_apply_min') ?? 'Bật Giao diện tối giản (Tắt 100% hiệu ứng kính mờ)', style: const TextStyle(color: Colors.white)),
                  subtitle: Text(L10n.t('opt_apply_min_sub') ?? 'Giúp app chạy siêu mượt trên các máy tính đời cũ.', style: const TextStyle(color: Colors.white54, fontSize: 13)),
                  value: _recMinimalist,
                  activeColor: Colors.blueAccent,
                  onChanged: (v) => setState(() {
                    _recMinimalist = v!;
                    if (v) _recAllEffects = false;
                  }),
                ),
                CheckboxListTile(
                  contentPadding: EdgeInsets.zero,
                  title: Text(L10n.t('opt_apply_amb') ?? 'Tắt hiệu ứng Hình nền mờ (Ambient Background)', style: const TextStyle(color: Colors.white)),
                  subtitle: Text(_result!.isBattery ? (L10n.t('opt_apply_amb_sub1') ?? 'Giảm tải đáng kể cho GPU giúp tiết kiệm Pin và tăng thời gian sử dụng.') : (L10n.t('opt_apply_amb_sub2') ?? 'Giải phóng tài nguyên đồ họa cho máy tính.'), style: const TextStyle(color: Colors.white54, fontSize: 13)),
                  value: _recDisableAmbient,
                  activeColor: Colors.blueAccent,
                  onChanged: (v) => setState(() {
                    _recDisableAmbient = v!;
                    if (v) _recAllEffects = false;
                  }),
                ),
                CheckboxListTile(
                  contentPadding: EdgeInsets.zero,
                  title: Text(L10n.t('opt_apply_trl') ?? 'Tắt Phát tự động Trailer', style: const TextStyle(color: Colors.white)),
                  subtitle: Text(_result!.isBattery ? (L10n.t('opt_apply_trl_sub1') ?? 'Giảm số vòng xoay ổ cứng và mạng để tiết kiệm Pin.') : (L10n.t('opt_apply_trl_sub2') ?? 'Giảm hiện tượng giật lag khi mở trang phim.'), style: const TextStyle(color: Colors.white54, fontSize: 13)),
                  value: _recDisableTrailer,
                  activeColor: Colors.blueAccent,
                  onChanged: (v) => setState(() {
                    _recDisableTrailer = v!;
                    if (v) _recAllEffects = false;
                  }),
                ),
                CheckboxListTile(
                  contentPadding: EdgeInsets.zero,
                  title: Text(L10n.t('opt_apply_audio') ?? 'Tắt hiệu ứng Trình phát Nhạc (Tiết kiệm pin)', style: const TextStyle(color: Colors.white)),
                  subtitle: Text(L10n.t('opt_apply_audio_sub') ?? 'Tắt Sóng âm và Đĩa than xoay giúp giảm tải CPU/GPU, kéo dài thời lượng sử dụng pin.', style: const TextStyle(color: Colors.white54, fontSize: 13)),
                  value: _recDisableAudioEffects,
                  activeColor: Colors.blueAccent,
                  onChanged: (v) => setState(() {
                    _recDisableAudioEffects = v!;
                    if (v) _recAllEffects = false;
                  }),
                ),
                CheckboxListTile(
                  contentPadding: EdgeInsets.zero,
                  title: Text(L10n.t('opt_apply_all') ?? 'Bật TOÀN BỘ hiệu ứng rực rỡ nhất', style: const TextStyle(color: Colors.white)),
                  subtitle: Text(L10n.t('opt_apply_all_sub') ?? 'Máy tính của bạn hoàn toàn đủ khỏe để xử lý mọi đồ họa nặng nhất của app.', style: const TextStyle(color: Colors.white54, fontSize: 13)),
                  value: _recAllEffects,
                  activeColor: Colors.blueAccent,
                  onChanged: (v) => setState(() {
                    _recAllEffects = v!;
                    if (v) {
                      _recMinimalist = false;
                      _recDisableAmbient = false;
                      _recDisableTrailer = false;
                      _recDisableAudioEffects = false;
                    }
                  }),
                ),
              ],
            ),
          ),
        ),
        
        const SizedBox(height: 24),
        // Nút
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              children: [
                TextButton.icon(
                  icon: const Icon(Icons.settings_backup_restore, color: Colors.white54, size: 20),
                  onPressed: _resetToDefault,
                  label: Text(L10n.t('opt_btn_default') ?? 'Mặc định', style: const TextStyle(color: Colors.white54)),
                ),
                const SizedBox(width: 8),
                TextButton.icon(
                  icon: const Icon(Icons.undo, color: Colors.white54, size: 20),
                  onPressed: _undoOptimization,
                  label: Text(L10n.t('opt_btn_undo') ?? 'Hoàn tác', style: const TextStyle(color: Colors.white54)),
                ),
              ],
            ),
            Row(
              children: [
                TextButton(
                  onPressed: () => Navigator.of(context).pop(),
                  child: Text(L10n.t('opt_btn_close') ?? 'Đóng', style: const TextStyle(color: Colors.white54, fontSize: 16)),
                ),
                const SizedBox(width: 16),
                ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blueAccent,
                    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  onPressed: _applyOptimization,
                  icon: const Icon(Icons.auto_awesome, color: Colors.white),
                  label: Text(L10n.t('optimizer_apply') ?? 'Áp dụng Tối ưu', style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
                ),
              ],
            ),
          ],
        ),
      ],
    );
  }
}

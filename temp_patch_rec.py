import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/widgets/optimizer_dialog.dart', 'r', encoding='utf-8') as f:
    content = f.read()

search = """    if (_result!.isBattery) {
       widgets.add(_buildRichLine(Icons.battery_alert, Colors.orangeAccent, 
         L10n.t('opt_bat_title') ?? "Đang dùng Pin: ", 
         L10n.t('opt_bat_desc') ?? "Nếu bạn muốn cày phim lâu hơn, hãy ưu tiên chọn chất lượng 1080p và đồng ý tắt bớt hiệu ứng nền (nếu có) để tiết kiệm điện."));
    } else if (_result!.resolution.height <= 1080) {"""

replace = """    if (_result!.isBattery) {
       widgets.add(_buildRichLine(Icons.battery_alert, Colors.orangeAccent, 
         L10n.t('opt_bat_title') ?? "Đang dùng Pin: ", 
         L10n.t('opt_bat_desc') ?? "Nếu bạn muốn cày phim lâu hơn, hãy ưu tiên chọn chất lượng 1080p và đồng ý tắt bớt hiệu ứng nền (nếu có). Ngoài ra, khi nghe nhạc, hãy tắt hiệu ứng Sóng âm và Đĩa than để tiết kiệm điện tối đa."));
    } else if (_result!.resolution.height <= 1080) {"""

if search in content:
    content = content.replace(search, replace)
    print("Injected battery audio recommendation!")

search2 = """    } else if (_result!.isLowEnd) {
       widgets.add(_buildRichLine(Icons.warning_amber, Colors.amber, 
         L10n.t('opt_low_end_title') ?? "Cấu hình khiêm tốn: ", 
         L10n.t('opt_low_end_desc') ?? "Hệ thống sẽ đề xuất tự động tắt bớt hiệu ứng kính mờ để trải nghiệm của bạn mượt mà nhất."));
    }"""

replace2 = """    } else if (_result!.isLowEnd) {
       widgets.add(_buildRichLine(Icons.warning_amber, Colors.amber, 
         L10n.t('opt_low_end_title') ?? "Cấu hình khiêm tốn: ", 
         L10n.t('opt_low_end_desc') ?? "Hệ thống sẽ đề xuất tự động tắt hiệu ứng kính mờ và các hiệu ứng sóng âm nhạc đồ hoạ nặng để trải nghiệm của bạn mượt mà nhất."));
    }"""

if search2 in content:
    content = content.replace(search2, replace2)
    print("Injected low end audio recommendation!")

with open('lib/widgets/optimizer_dialog.dart', 'w', encoding='utf-8') as f:
    f.write(content)

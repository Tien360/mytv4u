import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_dialog = """  void _showSleepTimerDialog() {
    showDialog(
      context: context,
      barrierColor: Colors.black.withOpacity(0.5),
      builder: (ctx) {
        return Center(
          child: Material(
            color: Colors.transparent,
            child: GlassContainer(
              width: 340,
              height: 380,
              borderRadius: 20,
              color: const Color(0x1A000000),
              borderColor: const Color(0x33FFFFFF),
              blur: 40.0,
              child: Column(
                children: [
                  Padding(
                    padding: const EdgeInsets.all(20),
                    child: Text(
                      L10n.t('sleep_timer') ?? 'Hẹn giờ tắt',
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  const Divider(color: Colors.white24, height: 1),
                  Expanded(
                    child: ListView(
                      children: [
                        _buildTimerOption(ctx, L10n.t('off') ?? 'Tắt', 0),
                        _buildTimerOption(ctx, '30 ${L10n.t('minutes') ?? 'phút'}', 30),
                        _buildTimerOption(ctx, '60 ${L10n.t('minutes') ?? 'phút'}', 60),
                        _buildTimerOption(ctx, '90 ${L10n.t('minutes') ?? 'phút'}', 90),
                        _buildTimerOption(ctx, '120 ${L10n.t('minutes') ?? 'phút'}', 120),
                        ListTile(
                          title: Text(L10n.t('custom') ?? 'Tùy chỉnh...', style: const TextStyle(color: Colors.white)),
                          trailing: const Icon(Icons.chevron_right, color: Colors.white54),
                          onTap: () {
                            Navigator.pop(ctx);
                            _showCustomSleepTimerDialog();
                          },
                        ),
                      ],
                    ),
                  ),
                  const Divider(color: Colors.white24, height: 1),
                  TextButton(
                    onPressed: () => Navigator.pop(ctx),
                    child: Padding(
                      padding: const EdgeInsets.all(12),
                      child: Text(
                        L10n.t('cancel') ?? 'Hủy',
                        style: const TextStyle(color: Colors.blueAccent, fontSize: 16),
                      ),
                    ),
                  )
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  Widget _buildTimerOption(BuildContext ctx, String label, int minutes) {
    bool isSelected = _sleepTimerMinutes == minutes;
    return ListTile(
      title: Text(
        label,
        style: TextStyle(
          color: isSelected ? Colors.blueAccent : Colors.white,
          fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
        ),
      ),
      trailing: isSelected ? const Icon(Icons.check, color: Colors.blueAccent) : null,
      onTap: () {
        setState(() {
          _sleepTimerMinutes = minutes;
          _sleepTimer?.cancel();
          if (minutes > 0) {
            _sleepTimer = Timer(Duration(minutes: minutes), () {
              if (mounted) {
                player.pause();
                Navigator.pop(context); // Thoát trình phát
              }
            });
          }
        });
        Navigator.pop(ctx);
      },
    );
  }

  void _showCustomSleepTimerDialog() {
    final TextEditingController _tc = TextEditingController(
      text: _sleepTimerMinutes > 0 ? _sleepTimerMinutes.toString() : '',
    );
    showDialog(
      context: context,
      barrierColor: Colors.black.withOpacity(0.5),
      builder: (ctx) {
        return Center(
          child: Material(
            color: Colors.transparent,
            child: GlassContainer(
              width: 320,
              height: 240,
              borderRadius: 20,
              color: const Color(0x1A000000),
              borderColor: const Color(0x33FFFFFF),
              blur: 40.0,
              child: Column(
                children: [
                  Padding(
                    padding: const EdgeInsets.all(20),
                    child: Text(
                      L10n.t('custom_timer') ?? 'Tùy chỉnh (phút)',
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  const Divider(color: Colors.white24, height: 1),
                  Padding(
                    padding: const EdgeInsets.all(20),
                    child: TextField(
                      controller: _tc,
                      keyboardType: TextInputType.number,
                      style: const TextStyle(color: Colors.white, fontSize: 24),
                      textAlign: TextAlign.center,
                      autofocus: true,
                      decoration: InputDecoration(
                        hintText: '0',
                        hintStyle: const TextStyle(color: Colors.white24),
                        enabledBorder: OutlineInputBorder(
                          borderSide: const BorderSide(color: Colors.white24),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderSide: const BorderSide(color: Colors.blueAccent),
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                    ),
                  ),
                  const Spacer(),
                  const Divider(color: Colors.white24, height: 1),
                  Row(
                    children: [
                      Expanded(
                        child: TextButton(
                          onPressed: () => Navigator.pop(ctx),
                          child: Padding(
                            padding: const EdgeInsets.all(12),
                            child: Text(
                              L10n.t('cancel') ?? 'Hủy',
                              style: const TextStyle(color: Colors.white54, fontSize: 16),
                            ),
                          ),
                        ),
                      ),
                      Container(width: 1, height: 48, color: Colors.white24),
                      Expanded(
                        child: TextButton(
                          onPressed: () {
                            final val = int.tryParse(_tc.text) ?? 0;
                            setState(() {
                              _sleepTimerMinutes = val;
                              _sleepTimer?.cancel();
                              if (val > 0) {
                                _sleepTimer = Timer(Duration(minutes: val), () {
                                  if (mounted) {
                                    player.pause();
                                    Navigator.pop(context); // Thoát trình phát
                                  }
                                });
                              }
                            });
                            Navigator.pop(ctx);
                          },
                          child: Padding(
                            padding: const EdgeInsets.all(12),
                            child: Text(
                              L10n.t('ok') ?? 'Xác nhận',
                              style: const TextStyle(color: Colors.blueAccent, fontSize: 16, fontWeight: FontWeight.bold),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }"""

pattern = r"  void _showSleepTimerDialog\(\) \{[\s\S]*?Navigator\.pop\(context\); // ThoAt trAnh phAt\s*\}\s*\}\);\s*\}\s*\}\);\s*Navigator\.pop\(ctx\);\s*\},[\s\S]*?\}\s*\)\s*\]\s*\)\s*;\s*\}\s*,\s*\)\s*;"
content = re.sub(pattern, new_dialog, content)

# I should also fix the language keys in the ListTile in tab_general where it says "Chất lượng video" and "Chế độ lặp lại"
# In player_screen.dart, replace raw Vietnamese strings with L10n keys where appropriate.
content = content.replace("const Text('Cht lng video', style: TextStyle(color: Colors.white))", "Text(L10n.t('video_quality') ?? 'Chất lượng video', style: const TextStyle(color: Colors.white))")
content = content.replace("const Text('?ang ti danh sAch...', style: TextStyle(color: Colors.white54, fontSize: 12))", "Text(L10n.t('loading') ?? 'Đang tải...', style: const TextStyle(color: Colors.white54, fontSize: 12))")
content = content.replace("const Text('Ch `T lp li', style: TextStyle(color: Colors.white))", "Text(L10n.t('repeat_mode') ?? 'Chế độ lặp lại', style: const TextStyle(color: Colors.white))")
content = content.replace("const Text('H1n gi? t_t', style: TextStyle(color: Colors.white))", "Text(L10n.t('sleep_timer') ?? 'Hẹn giờ tắt', style: const TextStyle(color: Colors.white))")
content = content.replace("'CAn li $_sleepTimerMinutes phAt'", "L10n.t('timer_remaining')?.replaceAll('%s', _sleepTimerMinutes.toString()) ?? 'Còn lại $_sleepTimerMinutes phút'")
content = content.replace("'?ang t_t'", "L10n.t('off') ?? 'Tắt'")
content = content.replace("const Text('T_t')", "Text(L10n.t('off') ?? 'Tắt')")
content = content.replace("const Text('Lp li danh sAch')", "Text(L10n.t('repeat_list') ?? 'Lặp lại danh sách')")
content = content.replace("const Text('Lp li 1 bAi')", "Text(L10n.t('repeat_one') ?? 'Lặp lại 1 bài')")
content = content.replace("h == 0 ? 'T `Tng (Cht lng cao nht)'", "h == 0 ? (L10n.t('auto_highest') ?? 'Tự động (Cao nhất)')")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated player_screen.dart timer UI")

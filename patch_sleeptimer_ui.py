import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

start_str = "  void _showSleepTimerDialog() {"
end_str = "  void _setSleepTimer(int minutes) {"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

new_methods = """  void _showSleepTimerDialog() {
    showDialog(
      context: context,
      barrierColor: Colors.black.withOpacity(0.5),
      builder: (context) {
        return Center(
          child: Material(
            color: Colors.transparent,
            child: GlassContainer(
              width: 350,
              height: 400,
              borderRadius: 24,
              padding: const EdgeInsets.all(24),
              color: const Color(0x1A000000),
              borderColor: const Color(0x33FFFFFF),
              blur: 40.0,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(L10n.t('sleep_timer') ?? 'Hẹn giờ tự động tắt', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 20, color: Colors.white)),
                  const SizedBox(height: 8),
                  const Text('Chọn khoảng thời gian để tự động dừng phát và thoát.', style: TextStyle(color: Colors.white70)),
                  const SizedBox(height: 24),
                  Expanded(
                    child: ListView(
                      children: [
                        _buildSleepOption(60),
                        _buildSleepOption(120),
                        _buildSleepOption(180),
                        ListTile(
                          title: const Text('Tùy chỉnh...', style: TextStyle(color: Colors.orange)),
                          onTap: () {
                            Navigator.pop(context);
                            _showCustomSleepTimerDialog();
                          },
                        ),
                      ],
                    ),
                  ),
                  if (_sleepSecondsRemaining > 0)
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        style: ElevatedButton.styleFrom(backgroundColor: Colors.redAccent, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8))),
                        onPressed: () {
                          Navigator.pop(context);
                          setState(() {
                            _sleepSecondsRemaining = 0;
                            _sleepTimer?.cancel();
                          });
                        },
                        child: Text(L10n.t('turn_off') ?? 'Tắt hẹn giờ'),
                      ),
                    ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  Widget _buildSleepOption(int minutes) {
    return ListTile(
      title: Text('$minutes phút', style: const TextStyle(color: Colors.blueAccent)),
      onTap: () {
        Navigator.pop(context);
        _setSleepTimer(minutes);
      },
    );
  }

  void _showCustomSleepTimerDialog() {
    int minutes = 0;
    showDialog(
      context: context,
      barrierColor: Colors.black.withOpacity(0.5),
      builder: (context) {
        return Center(
          child: Material(
            color: Colors.transparent,
            child: GlassContainer(
              width: 350,
              padding: const EdgeInsets.all(24),
              borderRadius: 24,
              color: const Color(0x1A000000),
              borderColor: const Color(0x33FFFFFF),
              blur: 40.0,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Tùy chỉnh thời gian', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20, color: Colors.white)),
                  const SizedBox(height: 16),
                  TextField(
                    keyboardType: TextInputType.number,
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      hintText: 'Nhập số phút',
                      hintStyle: const TextStyle(color: Colors.white54),
                      enabledBorder: OutlineInputBorder(borderSide: BorderSide(color: Colors.white24)),
                      focusedBorder: OutlineInputBorder(borderSide: BorderSide(color: Colors.blueAccent)),
                    ),
                    onChanged: (val) {
                      minutes = int.tryParse(val) ?? 0;
                    },
                  ),
                  const SizedBox(height: 24),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      TextButton(
                        child: const Text('Hủy', style: TextStyle(color: Colors.white70)),
                        onPressed: () => Navigator.pop(context),
                      ),
                      const SizedBox(width: 8),
                      ElevatedButton(
                        child: const Text('Đồng ý'),
                        onPressed: () {
                          Navigator.pop(context);
                          if (minutes > 0) _setSleepTimer(minutes);
                        },
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
  }

"""

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_methods + content[end_idx:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched sleep timer UI")
else:
    print("Could not find sleep timer methods")

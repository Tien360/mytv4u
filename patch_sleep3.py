import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_method = """  void _showSleepTimerDialog() {
    showDialog(
      context: context,
      builder: (ctx) {
        return AlertDialog(
          backgroundColor: Colors.grey[900],
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          title: Text(L10n.t('sleep_timer') ?? 'Hẹn giờ tự động tắt', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              _buildSleepOption(ctx, 60, '60 phút'),
              _buildSleepOption(ctx, 120, '120 phút'),
              _buildSleepOption(ctx, 180, '180 phút'),
              _buildSleepOption(ctx, -1, 'Tùy chỉnh...'),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () {
                setState(() {
                  _sleepTimerMinutes = 0;
                  _sleepTimer?.cancel();
                });
                Navigator.pop(ctx);
              },
              child: Text(L10n.t('turn_off') ?? 'Tắt', style: const TextStyle(color: Colors.redAccent)),
            ),
            TextButton(
              onPressed: () => Navigator.pop(ctx),
              child: const Text('Hủy', style: TextStyle(color: Colors.white54)),
            ),
          ],
        );
      },
    );
  }

  Widget _buildSleepOption(BuildContext ctx, int minutes, String label) {
    return ListTile(
      title: Text(label, style: const TextStyle(color: Colors.white)),
      trailing: (minutes > 0 && _sleepTimerMinutes == minutes) ? const Icon(Icons.check, color: Colors.blueAccent) : null,
      onTap: () {
        Navigator.pop(ctx);
        if (minutes == -1) {
          _showCustomSleepTimerDialog();
        } else {
          _setSleepTimer(minutes);
        }
      },
    );
  }

  void _showCustomSleepTimerDialog() {
    final TextEditingController _tc = TextEditingController(text: _sleepTimerMinutes > 0 ? _sleepTimerMinutes.toString() : '');
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: Colors.grey[900],
        title: const Text('Tùy chỉnh thời gian (phút)', style: TextStyle(color: Colors.white)),
        content: TextField(
          controller: _tc,
          keyboardType: TextInputType.number,
          style: const TextStyle(color: Colors.white),
          decoration: const InputDecoration(
            hintText: 'Nhập số phút...',
            hintStyle: TextStyle(color: Colors.white54),
            enabledBorder: OutlineInputBorder(borderSide: BorderSide(color: Colors.white24)),
            focusedBorder: OutlineInputBorder(borderSide: BorderSide(color: Colors.blueAccent)),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Hủy', style: TextStyle(color: Colors.white54)),
          ),
          TextButton(
            onPressed: () {
              final val = int.tryParse(_tc.text) ?? 0;
              Navigator.pop(ctx);
              if (val > 0) _setSleepTimer(val);
            },
            child: const Text('Đồng ý', style: TextStyle(color: Colors.blueAccent)),
          ),
        ],
      ),
    );
  }

  void _setSleepTimer(int minutes) {
    setState(() {
      _sleepTimerMinutes = minutes;
      _sleepTimer?.cancel();
      if (minutes > 0) {
        _sleepTimer = Timer(Duration(minutes: minutes), () {
          if (mounted) {
            player.pause();
            Navigator.pop(context);
          }
        });
      }
    });
  }

"""

start_str = "  void _showSleepTimerDialog() {"
end_str = "  void _playNextEpisode() {"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_method + content[end_idx:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced sleep timer successfully!")
else:
    print("Could not find start/end markers")

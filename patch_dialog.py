import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

search_tab1 = """                            children: [
                                ListTile(
                                  title: Text(L10n.t('playback_speed') ?? 'Tốc độ phát',"""

new_tab1 = """                            children: [
                                SwitchListTile(
                                  title: Text('Phát lặp lại (Repeat)', style: const TextStyle(color: Colors.white)),
                                  activeColor: Colors.blueAccent,
                                  value: _isRepeat,
                                  onChanged: (val) {
                                    setState(() {
                                      _isRepeat = val;
                                      player.setPlaylistMode(val ? PlaylistMode.single : PlaylistMode.none);
                                    });
                                    setTabState((){});
                                  },
                                ),
                                const Divider(color: Colors.white24),
                                ListTile(
                                  title: Text('Hẹn giờ tắt: ${_sleepTimerMinutes == 0 ? 'Tắt' : '$_sleepTimerMinutes phút'}', style: const TextStyle(color: Colors.white)),
                                  subtitle: _sleepEndTime != null 
                                      ? Text('Tắt lúc ${_sleepEndTime!.hour.toString().padLeft(2,'0')}:${_sleepEndTime!.minute.toString().padLeft(2,'0')}', style: const TextStyle(color: Colors.blueAccent)) 
                                      : null,
                                  trailing: DropdownButton<int>(
                                    dropdownColor: Colors.grey[900],
                                    value: _sleepTimerMinutes,
                                    style: const TextStyle(color: Colors.blueAccent),
                                    items: [0, 15, 30, 45, 60, 90, 120].map((m) {
                                      return DropdownMenuItem<int>(
                                        value: m,
                                        child: Text(m == 0 ? 'Tắt' : '$m phút'),
                                      );
                                    }).toList(),
                                    onChanged: (val) {
                                      if (val != null) {
                                        setState(() {
                                          _sleepTimerMinutes = val;
                                          _startSleepTimer();
                                        });
                                        setTabState((){});
                                      }
                                    },
                                  ),
                                ),
                                const Divider(color: Colors.white24),
                                ListTile(
                                  title: Text(L10n.t('playback_speed') ?? 'Tốc độ phát',"""

if "Phát lặp lại (Repeat)" not in content:
    content = content.replace(search_tab1, new_tab1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched settings dialog UI")
else:
    print("Already patched")

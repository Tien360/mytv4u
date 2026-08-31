import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

search_tab = """                                  const Divider(color: Colors.white24),
                                ],

                                ListTile(
                                  leading: const Icon("""
new_tab = """                                  const Divider(color: Colors.white24),
                                ],
                                
                                if (_ytQualities.length > 1) ...[
                                  ListTile(
                                    title: const Text('Chất lượng YouTube', style: TextStyle(color: Colors.white)),
                                    trailing: DropdownButton<int>(
                                      dropdownColor: Colors.grey[900],
                                      value: _selectedYtHeight,
                                      style: const TextStyle(color: Colors.blueAccent),
                                      items: _ytQualities.map((h) {
                                        return DropdownMenuItem<int>(
                                          value: h,
                                          child: Text(h == 0 ? 'Tự động (Chất lượng cao nhất)' : '${h}p'),
                                        );
                                      }).toList(),
                                      onChanged: (val) {
                                        if (val != null) {
                                          _changeYtQuality(val);
                                          setTabState(() {});
                                        }
                                      },
                                    ),
                                  ),
                                  const Divider(color: Colors.white24),
                                ],
                                
                                ListTile(
                                  leading: const Icon(Icons.repeat, color: Colors.blueAccent),
                                  title: const Text('Chế độ lặp lại', style: TextStyle(color: Colors.white)),
                                  trailing: DropdownButton<int>(
                                    dropdownColor: Colors.grey[900],
                                    value: _repeatMode,
                                    style: const TextStyle(color: Colors.blueAccent),
                                    items: const [
                                      DropdownMenuItem(value: 0, child: Text('Tắt')),
                                      DropdownMenuItem(value: 1, child: Text('Lặp lại danh sách')),
                                      DropdownMenuItem(value: 2, child: Text('Lặp lại 1 bài')),
                                    ],
                                    onChanged: (val) {
                                      if (val != null) {
                                        setState(() => _repeatMode = val);
                                        setTabState(() {});
                                      }
                                    },
                                  ),
                                ),
                                const Divider(color: Colors.white24),
                                
                                ListTile(
                                  leading: Icon(Icons.timer, color: _sleepTimerMinutes > 0 ? Colors.blueAccent : Colors.blueAccent),
                                  title: const Text('Hẹn giờ tắt', style: TextStyle(color: Colors.white)),
                                  subtitle: Text(_sleepTimerMinutes > 0 ? 'Còn lại $_sleepTimerMinutes phút' : 'Đang tắt', style: const TextStyle(color: Colors.white54)),
                                  trailing: const Icon(Icons.chevron_right, color: Colors.white54),
                                  onTap: () {
                                    Navigator.pop(context);
                                    _showSleepTimerDialog();
                                  },
                                ),
                                const Divider(color: Colors.white24),

                                ListTile(
                                  leading: const Icon("""

if "'Chất lượng YouTube'" not in content:
    content = content.replace(search_tab, new_tab)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Step 2 done")

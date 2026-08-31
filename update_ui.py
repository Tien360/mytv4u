import os
import re

content = open("lib/screens/audio_player_screen.dart", "r", encoding="utf-8").read()

# 1. Add _showAudioSettings method
settings_method = '''
  void _showAudioSettings() {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      builder: (context) => StatefulBuilder(
        builder: (context, setSheetState) {
          return Container(
            decoration: BoxDecoration(
              color: Colors.grey[900]?.withOpacity(0.95),
              borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
              border: Border(top: BorderSide(color: Colors.white.withOpacity(0.1))),
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const SizedBox(height: 12),
                Container(width: 40, height: 5, decoration: BoxDecoration(color: Colors.grey[600], borderRadius: BorderRadius.circular(10))),
                const SizedBox(height: 16),
                const Text("Cài đặt Trình phát", style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                const SizedBox(height: 16),
                ListTile(
                  leading: const Icon(Icons.graphic_eq, color: Colors.white70),
                  title: const Text('Hiệu ứng sóng âm', style: TextStyle(color: Colors.white)),
                  trailing: DropdownButton<String>(
                    dropdownColor: Colors.grey[850],
                    value: visualizerType,
                    underline: const SizedBox(),
                    items: const [
                      DropdownMenuItem(value: 'bars', child: Text('Cột sóng', style: TextStyle(color: Colors.white))),
                      DropdownMenuItem(value: 'waves', child: Text('Lượn sóng', style: TextStyle(color: Colors.white))),
                    ],
                    onChanged: (val) async {
                      if (val != null) {
                        final prefs = await SharedPreferences.getInstance();
                        prefs.setString('audio_visualizer', val);
                        setSheetState(() => visualizerType = val);
                        setState(() => visualizerType = val);
                      }
                    },
                  ),
                ),
                ListTile(
                  leading: const Icon(Icons.timer, color: Colors.white70),
                  title: const Text('Hẹn giờ tắt (phút)', style: TextStyle(color: Colors.white)),
                  trailing: DropdownButton<int>(
                    dropdownColor: Colors.grey[850],
                    value: sleepTimerMinutes,
                    underline: const SizedBox(),
                    items: const [
                      DropdownMenuItem(value: 0, child: Text('Tắt', style: TextStyle(color: Colors.white))),
                      DropdownMenuItem(value: 15, child: Text('15', style: TextStyle(color: Colors.white))),
                      DropdownMenuItem(value: 30, child: Text('30', style: TextStyle(color: Colors.white))),
                      DropdownMenuItem(value: 60, child: Text('60', style: TextStyle(color: Colors.white))),
                    ],
                    onChanged: (val) async {
                      if (val != null) {
                        final prefs = await SharedPreferences.getInstance();
                        prefs.setInt('audio_sleep_timer', val);
                        setSheetState(() => sleepTimerMinutes = val);
                        setState(() => sleepTimerMinutes = val);
                        if (val > 0) {
                          Future.delayed(Duration(minutes: val), () {
                            if (mounted) player.pause();
                          });
                        }
                      }
                    },
                  ),
                ),
                ListTile(
                  leading: const Icon(Icons.repeat, color: Colors.white70),
                  title: const Text('Chế độ lặp lại', style: TextStyle(color: Colors.white)),
                  trailing: DropdownButton<int>(
                    dropdownColor: Colors.grey[850],
                    value: repeatMode,
                    underline: const SizedBox(),
                    items: const [
                      DropdownMenuItem(value: 0, child: Text('Không lặp', style: TextStyle(color: Colors.white))),
                      DropdownMenuItem(value: 1, child: Text('Lặp danh sách', style: TextStyle(color: Colors.white))),
                      DropdownMenuItem(value: 2, child: Text('Lặp 1 bài', style: TextStyle(color: Colors.white))),
                    ],
                    onChanged: (val) {
                      if (val != null) {
                        setSheetState(() => repeatMode = val);
                        setState(() => repeatMode = val);
                      }
                    },
                  ),
                ),
                const SizedBox(height: 32),
              ],
            ),
          );
        }
      )
    );
  }
'''

if "_showAudioSettings()" not in content:
    content = content.replace("  @override\n  Widget build(BuildContext context) {", settings_method + "\n  @override\n  Widget build(BuildContext context) {")


# 2. Update settings icon onPressed
content = content.replace("""                          IconButton(
                            icon: const Icon(Icons.settings, color: Colors.white),
                            onPressed: () {
                              Navigator.push(context, MaterialPageRoute(builder: (_) => const SettingsScreen())).then((_) {
                                _loadSettings();
                              });
                            },
                          ),""", """                          IconButton(
                            icon: const Icon(Icons.settings, color: Colors.white),
                            onPressed: _showAudioSettings,
                          ),""")

# 3. Update Playlist UI
old_playlist = """                          IconButton(
                            icon: const Icon(Icons.queue_music, color: Colors.white),
                            onPressed: () {
                              showModalBottomSheet(
                                context: context,
                                backgroundColor: Colors.transparent,
                                builder: (context) => Container(
                                  decoration: BoxDecoration(
                                    color: Colors.grey[900],
                                    borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
                                  ),
                                  child: Column(
                                    children: [
                                      const SizedBox(height: 12),
                                      Container(width: 40, height: 5, decoration: BoxDecoration(color: Colors.grey[600], borderRadius: BorderRadius.circular(10))),
                                      const SizedBox(height: 16),
                                      Text(L10n.t('playlist') ?? "Danh sách phát", style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                                      const SizedBox(height: 16),
                                      Expanded(
                                        child: ListView.builder(
                                          itemCount: widget.files.length,
                                          itemBuilder: (context, index) {
                                            bool active = index == currentIndex;
                                            return ListTile(
                                              leading: Icon(active ? Icons.volume_up : Icons.music_note, color: active ? Colors.blueAccent : Colors.white54),
                                              title: Text(
                                                widget.files[index].name.replaceAll(RegExp(r'\.[a-zA-Z0-9]+$'), ''),
                                                style: TextStyle(color: active ? Colors.blueAccent : Colors.white, fontWeight: active ? FontWeight.bold : FontWeight.normal),
                                              ),
                                              onTap: () {
                                                Navigator.pop(context);
                                                currentIndex = index;
                                                _loadCurrent();
                                              },
                                            );
                                          }
                                        ),
                                      ),
                                    ],
                                  ),
                                )
                              );
                            },
                          ),"""

new_playlist = """                          IconButton(
                            icon: const Icon(Icons.queue_music, color: Colors.white),
                            onPressed: () {
                              showModalBottomSheet(
                                context: context,
                                backgroundColor: Colors.transparent,
                                isScrollControlled: true,
                                builder: (context) => FractionallySizedBox(
                                  heightFactor: 0.7,
                                  child: ClipRRect(
                                    borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
                                    child: BackdropFilter(
                                      filter: ImageFilter.blur(sigmaX: 30, sigmaY: 30),
                                      child: Container(
                                        decoration: BoxDecoration(
                                          color: Colors.black.withOpacity(0.6),
                                          border: Border(top: BorderSide(color: Colors.white.withOpacity(0.2))),
                                        ),
                                        child: Column(
                                          children: [
                                            const SizedBox(height: 12),
                                            Container(width: 40, height: 5, decoration: BoxDecoration(color: Colors.white38, borderRadius: BorderRadius.circular(10))),
                                            const SizedBox(height: 16),
                                            Text(L10n.t('playlist') ?? "Danh sách phát", style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold, letterSpacing: 1.2)),
                                            const SizedBox(height: 16),
                                            Expanded(
                                              child: ListView.builder(
                                                itemCount: widget.files.length,
                                                itemBuilder: (context, index) {
                                                  bool active = index == currentIndex;
                                                  return Container(
                                                    margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                                                    decoration: BoxDecoration(
                                                      color: active ? Colors.white.withOpacity(0.1) : Colors.transparent,
                                                      borderRadius: BorderRadius.circular(12),
                                                    ),
                                                    child: ListTile(
                                                      contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                                                      leading: Container(
                                                        width: 48,
                                                        height: 48,
                                                        decoration: BoxDecoration(
                                                          color: Colors.grey[850],
                                                          borderRadius: BorderRadius.circular(8),
                                                        ),
                                                        child: active
                                                            ? const Icon(Icons.equalizer, color: Colors.blueAccent)
                                                            : const Icon(Icons.music_note, color: Colors.white54),
                                                      ),
                                                      title: Text(
                                                        widget.files[index].name.replaceAll(RegExp(r'\.[a-zA-Z0-9]+$'), ''),
                                                        style: TextStyle(color: active ? Colors.blueAccent : Colors.white, fontWeight: active ? FontWeight.bold : FontWeight.normal, fontSize: 16),
                                                        maxLines: 1,
                                                        overflow: TextOverflow.ellipsis,
                                                      ),
                                                      onTap: () {
                                                        Navigator.pop(context);
                                                        currentIndex = index;
                                                        _loadCurrent();
                                                      },
                                                    ),
                                                  );
                                                }
                                              ),
                                            ),
                                          ],
                                        ),
                                      ),
                                    ),
                                  ),
                                )
                              );
                            },
                          ),"""

# Note: We replace the exact old string
content = content.replace(old_playlist, new_playlist)

# 4. Update Vinyl Disc design (Picture Disc style)
old_vinyl = """                                  child: Container(
                                    width: 320,
                                    height: 320,
                                    decoration: BoxDecoration(
                                      shape: BoxShape.circle,
                                      color: const Color(0xFF121212),
                                      boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 40, offset: Offset(0, 20))],
                                      border: Border.all(color: Colors.white12, width: 1),
                                    ),
                                    child: Stack(
                                      alignment: Alignment.center,
                                      children: [
                                        // Vinyl grooves
                                        for (double w = 300; w > 120; w -= 20)
                                          Container(
                                            width: w,
                                            height: w,
                                            decoration: BoxDecoration(
                                              shape: BoxShape.circle,
                                              border: Border.all(color: Colors.white.withOpacity(0.03), width: 1.5),
                                            ),
                                          ),
                                        // Center label
                                        Container(
                                          width: 130,
                                          height: 130,
                                          decoration: BoxDecoration(
                                            shape: BoxShape.circle,
                                            image: coverArt != null
                                                ? DecorationImage(image: MemoryImage(coverArt!), fit: BoxFit.cover)
                                                : null,
                                            color: Colors.grey[900],
                                          ),
                                          child: coverArt == null ? const Icon(Icons.music_note, size: 50, color: Colors.white24) : null,
                                        ),
                                        // Spindle hole
                                        Container(
                                          width: 12,
                                          height: 12,
                                          decoration: const BoxDecoration(shape: BoxShape.circle, color: Colors.black),
                                        ),
                                      ],
                                    ),
                                  ),"""

new_vinyl = """                                  child: Container(
                                    width: 320,
                                    height: 320,
                                    decoration: BoxDecoration(
                                      shape: BoxShape.circle,
                                      color: const Color(0xFF1A1A1A),
                                      image: coverArt != null
                                          ? DecorationImage(image: MemoryImage(coverArt!), fit: BoxFit.cover)
                                          : null,
                                      boxShadow: const [BoxShadow(color: Colors.black87, blurRadius: 50, offset: Offset(0, 25))],
                                      border: Border.all(color: Colors.white24, width: 2),
                                    ),
                                    child: Stack(
                                      alignment: Alignment.center,
                                      children: [
                                        // Overlay to darken image slightly so grooves are visible
                                        if (coverArt != null)
                                          Container(
                                            decoration: BoxDecoration(
                                              shape: BoxShape.circle,
                                              color: Colors.black.withOpacity(0.2),
                                            ),
                                          ),
                                        // Vinyl grooves on top of the image
                                        for (double w = 310; w > 50; w -= 15)
                                          Container(
                                            width: w,
                                            height: w,
                                            decoration: BoxDecoration(
                                              shape: BoxShape.circle,
                                              border: Border.all(color: Colors.black.withOpacity(0.15), width: 1),
                                            ),
                                          ),
                                        // Shine reflection
                                        Container(
                                          decoration: BoxDecoration(
                                            shape: BoxShape.circle,
                                            gradient: LinearGradient(
                                              begin: Alignment.topLeft,
                                              end: Alignment.bottomRight,
                                              colors: [
                                                Colors.white.withOpacity(0.4),
                                                Colors.transparent,
                                                Colors.transparent,
                                                Colors.white.withOpacity(0.1),
                                              ],
                                              stops: const [0.0, 0.3, 0.7, 1.0],
                                            ),
                                          ),
                                        ),
                                        // Spindle hole
                                        Container(
                                          width: 16,
                                          height: 16,
                                          decoration: BoxDecoration(
                                            shape: BoxShape.circle,
                                            color: Colors.black,
                                            border: Border.all(color: Colors.white54, width: 1),
                                            boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 4, offset: Offset(0, 2))],
                                          ),
                                        ),
                                        if (coverArt == null)
                                          const Icon(Icons.music_note, size: 80, color: Colors.white24),
                                      ],
                                    ),
                                  ),"""

content = content.replace(old_vinyl, new_vinyl)

open("lib/screens/audio_player_screen.dart", "w", encoding="utf-8").write(content)

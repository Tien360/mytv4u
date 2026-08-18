import re

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix 'Ä ang chá» n:' (Đang chọn:) tooltips
text = re.sub(r"'Ä ang chá» n: \$\{_selectedAudioTrack != null \? _getTrackShortName\(_selectedAudioTrack\) : \"Tá»± Ä‘á»™ng\"\}'", 
              r"'\\'", text)
text = re.sub(r"'Ä ang chá» n: \$\{_selectedSubtitleTrack != null \? _getTrackShortName\(_selectedSubtitleTrack\) : \"Tá»± Ä‘á»™ng\"\}'", 
              r"'\\'", text)
text = re.sub(r"'Ä ang chá» n: \$\{_selectedSecondarySubtitleTrack != null \? _getTrackShortName\(_selectedSecondarySubtitleTrack\) : \"Táº¯t\"\}'", 
              r"'\\'", text)

# 2. Fix 'CÃ i Ä‘áº·t' (Cài đặt) tooltip
text = text.replace("tooltip: 'CÃ i Ä‘áº·t',", "tooltip: L10n.t('settings_tooltip') ?? 'Settings',")

# 3. Replace episode GridView with Wrap
grid_start = '''                        Expanded(
                          child: GridView.builder(
                            gridDelegate:
                                const SliverGridDelegateWithFixedCrossAxisCount(
                                  crossAxisCount: 4,
                                  crossAxisSpacing: 8,
                                  mainAxisSpacing: 8,
                                  childAspectRatio: 1.5,
                                ),
                            itemCount: widget.episodes.length,
                            itemBuilder: (context, index) {
                              final isCurrent = index == _currentIndex;
                              return Material(
                                color: Colors.transparent,
                                child: InkWell(
                                  borderRadius: BorderRadius.circular(8),
                                  onTap: () {
                                    _initEpisode(index);
                                    setState(() => _showEpisodePanel = false);
                                  },
                                  child: Container(
                                    decoration: BoxDecoration(
                                      color: isCurrent
                                          ? Colors.blueAccent.withOpacity(0.4)
                                          : Colors.white10,
                                      borderRadius: BorderRadius.circular(8),
                                      border: Border.all(
                                        color: isCurrent
                                            ? Colors.blueAccent
                                            : Colors.transparent,
                                      ),
                                    ),
                                    alignment: Alignment.center,
                                    child: Text(
                                      widget.episodes[index].name,
                                      style: TextStyle(
                                        color: isCurrent
                                            ? Colors.blueAccent
                                            : Colors.white,
                                        fontWeight: isCurrent
                                            ? FontWeight.bold
                                            : FontWeight.normal,
                                      ),
                                    ),
                                  ),
                                ),
                              );
                            },
                          ),
                        ),'''
wrap_replacement = '''                        Expanded(
                          child: SingleChildScrollView(
                            child: Wrap(
                              spacing: 8,
                              runSpacing: 8,
                              children: widget.episodes.asMap().entries.map((entry) {
                                final index = entry.key;
                                final ep = entry.value;
                                final isCurrent = index == _currentIndex;
                                return Material(
                                  color: Colors.transparent,
                                  child: InkWell(
                                    borderRadius: BorderRadius.circular(8),
                                    onTap: () {
                                      _initEpisode(index);
                                      setState(() => _showEpisodePanel = false);
                                    },
                                    child: Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                                      decoration: BoxDecoration(
                                        color: isCurrent
                                            ? Colors.blueAccent.withOpacity(0.4)
                                            : Colors.white10,
                                        borderRadius: BorderRadius.circular(8),
                                        border: Border.all(
                                          color: isCurrent
                                              ? Colors.blueAccent
                                              : Colors.transparent,
                                        ),
                                      ),
                                      child: Text(
                                        ep.name,
                                        style: TextStyle(
                                          color: isCurrent
                                              ? Colors.blueAccent
                                              : Colors.white,
                                          fontWeight: isCurrent
                                              ? FontWeight.bold
                                              : FontWeight.normal,
                                        ),
                                      ),
                                    ),
                                  ),
                                );
                              }).toList(),
                            ),
                          ),
                        ),'''

text = text.replace(grid_start, wrap_replacement)

with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

with open('lib/widgets/advanced_controls_panel.dart', 'r', encoding='utf-8') as f:
    text2 = f.read()

# Fix valStr
old_valStr = "String valStr = isMs ? ' ms' : '';"
new_valStr = "String valStr = isMs ? ' ms' : value.toInt().toString();"
text2 = text2.replace(old_valStr, new_valStr)

with open('lib/widgets/advanced_controls_panel.dart', 'w', encoding='utf-8') as f:
    f.write(text2)

print("Updated player_screen and advanced_controls_panel!")

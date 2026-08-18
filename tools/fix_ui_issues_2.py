import sys

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Tooltips
old_audio = "'Đang chọn: '"
new_audio = "L10n.t('currently_selected')! + ''"
text = text.replace(old_audio, new_audio)

old_sub = "'Đang chọn: '"
new_sub = "L10n.t('currently_selected')! + ''"
text = text.replace(old_sub, new_sub)

old_sec_sub = "'Đang chọn: '"
new_sec_sub = "L10n.t('currently_selected')! + ''"
text = text.replace(old_sec_sub, new_sec_sub)

text = text.replace("tooltip: 'Cài đặt',", "tooltip: L10n.t('settings_tooltip') ?? 'Settings',")

# 2. Episode list Wrap
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
                                            ? Colors.blueAccent.withValues(alpha: 0.4)
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

print("Restored and updated!")

import sys, re
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

# Replace badge icon
badge_pattern = r"(_buildBadgeIcon\(\s*Icons\.layers,\s*episodeText,\s*\),)"
badge_replacement = r"""\1
                                              if (isSeries) ...[
                                                const SizedBox(width: 12),
                                                InkWell(
                                                  onTap: _showAirScheduleModal,
                                                  borderRadius: BorderRadius.circular(6),
                                                  child: Container(
                                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                                    decoration: BoxDecoration(
                                                      color: Colors.white.withOpacity(0.15),
                                                      borderRadius: BorderRadius.circular(6),
                                                      border: Border.all(color: Colors.white.withOpacity(0.3)),
                                                    ),
                                                    child: Row(
                                                      mainAxisSize: MainAxisSize.min,
                                                      children: [
                                                        const Icon(Icons.calendar_month, color: Colors.blueAccent, size: 16),
                                                        const SizedBox(width: 4),
                                                        Text(L10n.t('air_schedule') ?? 'Lịch phát sóng', style: const TextStyle(color: Colors.blueAccent, fontSize: 13, fontWeight: FontWeight.bold)),
                                                      ],
                                                    ),
                                                  ),
                                                ),
                                              ],"""

if re.search(badge_pattern, c):
    c = re.sub(badge_pattern, badge_replacement, c)
    print("Replaced badge")
else:
    print("Pattern not found")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)


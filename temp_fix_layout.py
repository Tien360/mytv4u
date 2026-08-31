import sys, re
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

# 1. Remove the button from the top
bad_button_pattern = r"""\s*if\s*\(isSeries\)\s*\.\.\.\[\s*const\s*SizedBox\(width:\s*12\),\s*InkWell\([\s\S]*?Text\(L10n\.t\('air_schedule'\) \?\? 'Lịch phát sóng'[\s\S]*?\]\,"""

c = re.sub(bad_button_pattern, "", c)

# 2. Add it next to _buildRichText for status
status_pattern = r"(if \(_tmdbDetails!\['status'\] != null\)\s*)(_buildRichText\('\$\{L10n\.t\('status'\) \?\? '.*?'\}: ', _translateStatus\(_tmdbDetails!\['status'\]\.toString\(\)\)\),)"

status_replacement = r"""\1
                                              Row(
                                                children: [
                                                  \2
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
                                                  ],
                                                ],
                                              ),"""

c = re.sub(status_pattern, status_replacement, c)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Fixed layout")

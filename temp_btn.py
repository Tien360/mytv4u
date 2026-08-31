import sys, re
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

pattern = r"(if \(isSeries\) \.\.\.\[\s*const SizedBox\(width: 12\),\s*InkWell\([\s\S]*?Text\(L10n\.t\('air_schedule'\)[^\)]*\),\s*\]\,\s*\)\,\s*\)\,\s*\]\,\s*\]\,)"
# wait, my button code currently looks like:
"""
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
"""

replacement = """                                                  if (isSeries) ...[
                                                    const SizedBox(width: 12),
                                                    Material(
                                                      color: Colors.transparent,
                                                      child: InkWell(
                                                        onTap: _showAirScheduleModal,
                                                        borderRadius: BorderRadius.circular(20),
                                                        child: Container(
                                                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                                          decoration: BoxDecoration(
                                                            color: Colors.white.withOpacity(0.08),
                                                            borderRadius: BorderRadius.circular(20),
                                                            border: Border.all(color: Colors.white.withOpacity(0.15)),
                                                          ),
                                                          child: Row(
                                                            mainAxisSize: MainAxisSize.min,
                                                            children: [
                                                              Icon(Icons.calendar_month_outlined, color: Colors.white.withOpacity(0.8), size: 15),
                                                              const SizedBox(width: 6),
                                                              Text(
                                                                L10n.t('air_schedule') ?? 'Lịch phát sóng', 
                                                                style: TextStyle(color: Colors.white.withOpacity(0.9), fontSize: 13, fontWeight: FontWeight.w500),
                                                              ),
                                                            ],
                                                          ),
                                                        ),
                                                      ),
                                                    ),
                                                  ],"""

c = re.sub(r"if \(isSeries\) \.\.\.\[.*?Text\(L10n\.t\('air_schedule'\)[^\)]*\).*?\]\,\s*\)\,\s*\)\,\s*\]\,", replacement, c, flags=re.DOTALL)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Updated button style")

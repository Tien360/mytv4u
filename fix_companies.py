import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

target = """Wrap(
                                                spacing: 12,
                                                runSpacing: 12,
                                                children: (_tmdbDetails!['production_companies'] as List)
                                                    .where((c) => c['logo_path'] != null)
                                                    .map((c) => AnimatedLogoWidget(logoPath: c['logo_path']))
                                                    .toList(),
                                              ),"""

replacement = """Wrap(
                                                spacing: 12,
                                                runSpacing: 12,
                                                crossAxisAlignment: WrapCrossAlignment.center,
                                                children: (_tmdbDetails!['production_companies'] as List)
                                                    .map<Widget>((c) {
                                                      if (c['logo_path'] != null) {
                                                        return AnimatedLogoWidget(logoPath: c['logo_path']);
                                                      } else {
                                                        return Container(
                                                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                                                          decoration: BoxDecoration(
                                                            color: Colors.white.withOpacity(0.1),
                                                            borderRadius: BorderRadius.circular(8),
                                                            border: Border.all(color: Colors.white.withOpacity(0.2)),
                                                          ),
                                                          child: Text(
                                                            c['name'] ?? '',
                                                            style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w500),
                                                          ),
                                                        );
                                                      }
                                                    })
                                                    .toList(),
                                              ),"""

text = text.replace(target, replacement)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated company logic")

import sys
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

target = """                                                  ],
                                ),
                              const SizedBox(height: 60),"""

replacement = """                                                  ],
                                                ],
                                              ),
                                              if (_tmdbDetails!['production_companies'] != null && (_tmdbDetails!['production_companies'] as List).isNotEmpty) ...[
                                                const SizedBox(height: 16),
                                                Text(
                                                  '${L10n.t('production_companies') ?? 'Hãng sản xuất'}:',
                                                  style: const TextStyle(
                                                    color: Colors.white,
                                                    fontWeight: FontWeight.bold,
                                                    fontSize: 15,
                                                  ),
                                                ),
                                                const SizedBox(height: 8),
                                                Wrap(
                                                  spacing: 12,
                                                  runSpacing: 12,
                                                  children: (_tmdbDetails!['production_companies'] as List).map((company) {
                                                    final logoPath = company['logo_path'];
                                                    if (logoPath != null) {
                                                      return Container(
                                                        height: 30,
                                                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                                        decoration: BoxDecoration(
                                                          color: Colors.white,
                                                          borderRadius: BorderRadius.circular(4),
                                                        ),
                                                        child: Image.network(
                                                          'https://image.tmdb.org/t/p/w200$logoPath',
                                                          height: 22,
                                                          fit: BoxFit.contain,
                                                        ),
                                                      );
                                                    }
                                                    return Text(
                                                      company['name'],
                                                      style: const TextStyle(color: Colors.white70),
                                                    );
                                                  }).toList(),
                                                ),
                                              ],
                                            ],
                                          ),
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              const SizedBox(height: 60),"""

if target in c:
    c = c.replace(target, replacement)
    print("Fixed missing brackets")
else:
    print("Target not found")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)


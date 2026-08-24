import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Fix gap above Trạng thái
text = text.replace("const SizedBox(height: 16),\n                                                const SizedBox(height: 32),\n                                            if (_tmdbDetails != null) ...[", 
                    "const SizedBox(height: 16),\n                                            if (_tmdbDetails != null) ...[")

text = text.replace("const SizedBox(height: 32),\n                                            if (_tmdbDetails != null) ...[", 
                    "const SizedBox(height: 16),\n                                            if (_tmdbDetails != null) ...[")

# Remove the trailing SizedBox from production_companies
text = text.replace("""                                              ),
                                              const SizedBox(height: 16),
                                            ],""",
"""                                              ),
                                            ],""")

# Remove the trailing SizedBox from next_episode_to_air
text = text.replace("""                                                      _buildRichText(L10n.t('next_episode') ?? 'Tp tip theo: ', '$airDateStr$extraText'),
                                                    ],
                                                  );
                                                }
                                              )
                                            ],""",
"""                                                      _buildRichText(L10n.t('next_episode') ?? 'Tập tiếp theo: ', '$airDateStr$extraText'),
                                                    ],
                                                  );
                                                }
                                              )
                                            ],""")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Fixed spacing!")

import re
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

finance_ui = """
                                            if (_tmdbDetails != null && _tmdbDetails!['budget'] != null && _tmdbDetails!['budget'] > 0 && _tmdbDetails!['revenue'] != null && _tmdbDetails!['revenue'] > 0) ...[
                                              const SizedBox(height: 32),
                                              Text(
                                                'Doanh thu / Kinh phí',
                                                style: const TextStyle(
                                                  color: Colors.white,
                                                  fontWeight: FontWeight.bold,
                                                  fontSize: 16,
                                                ),
                                              ),
                                              const SizedBox(height: 12),
                                              Column(
                                                crossAxisAlignment: CrossAxisAlignment.start,
                                                children: [
                                                  Row(
                                                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                                    children: [
                                                      Text(
                                                        '\\$${(_tmdbDetails!['budget'] / 1000000).toStringAsFixed(1)}M',
                                                        style: const TextStyle(color: Colors.white70, fontSize: 13),
                                                      ),
                                                      Text(
                                                        '\\$${(_tmdbDetails!['revenue'] / 1000000).toStringAsFixed(1)}M',
                                                        style: const TextStyle(color: Colors.greenAccent, fontSize: 13, fontWeight: FontWeight.bold),
                                                      ),
                                                    ],
                                                  ),
                                                  const SizedBox(height: 6),
                                                  ClipRRect(
                                                    borderRadius: BorderRadius.circular(4),
                                                    child: LinearProgressIndicator(
                                                      value: (_tmdbDetails!['budget'] / _tmdbDetails!['revenue']).clamp(0.0, 1.0),
                                                      backgroundColor: Colors.greenAccent.withOpacity(0.3),
                                                      valueColor: AlwaysStoppedAnimation<Color>(Colors.redAccent),
                                                      minHeight: 8,
                                                    ),
                                                  ),
                                                  const SizedBox(height: 4),
                                                  Text(
                                                    _tmdbDetails!['revenue'] > _tmdbDetails!['budget'] 
                                                        ? 'Lợi nhuận x${(_tmdbDetails!['revenue'] / _tmdbDetails!['budget']).toStringAsFixed(1)}'
                                                        : 'Lỗ vốn',
                                                    style: TextStyle(
                                                      color: _tmdbDetails!['revenue'] > _tmdbDetails!['budget'] ? Colors.greenAccent : Colors.redAccent,
                                                      fontSize: 12,
                                                    ),
                                                  ),
                                                ],
                                              ),
                                            ],
"""

pattern = r"(children: _directorsTmdb\.take\(3\)\.map.*?\)\.toList\(\),\s*\),\s*\]\,\s*)"
if re.search(pattern, content, flags=re.DOTALL):
    content = re.sub(pattern, lambda m: m.group(1) + finance_ui, content, count=1, flags=re.DOTALL)
    with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("Added finance UI")
else:
    print("Could not find target")

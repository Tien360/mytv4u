import re

with open("lib/widgets/air_schedule_dialog.dart", "r", encoding="utf-8") as f:
    c = f.read()

# Add import
c = c.replace("import '../api/tmdb_api.dart';", "import '../api/tmdb_api.dart';\nimport '../api/translate_api.dart';")

# Add state variables
c = c.replace("bool _isExpanded = false;", "bool _isExpanded = false;\n  bool _isTranslating = false;\n  String? _translatedOverview;")

# Update onTap logic
new_ontap = """      onTap: () async {
        setState(() {
          _isExpanded = !_isExpanded;
        });
        if (_isExpanded && widget.ep['_needs_translation'] == true && _translatedOverview == null && !_isTranslating) {
          setState(() { _isTranslating = true; });
          final res = await TranslateApi.translateEnToVi(widget.ep['overview'] ?? '');
          if (mounted) {
            setState(() {
              _translatedOverview = res;
              _isTranslating = false;
            });
          }
        }
      },"""
c = re.sub(r"      onTap: \(\) \{\s+setState\(\(\) \{\s+_isExpanded = !_isExpanded;\s+\}\);\s+\},", new_ontap, c)

# Update overview text rendering
# There are two places overview is rendered: one truncated when !_isExpanded, and one full when _isExpanded.
# In truncated, we just show original overview (English).
# In full, we show translated overview if available.

full_overview_block = """                          if (overview.isNotEmpty)
                            Text(
                              overview,
                              style: const TextStyle(color: Colors.white70, fontSize: 14, height: 1.6),
                            ),"""
                            
translated_block = """                          if (overview.isNotEmpty)
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  _translatedOverview ?? overview,
                                  style: const TextStyle(color: Colors.white70, fontSize: 14, height: 1.6),
                                ),
                                if (_isTranslating)
                                  const Padding(
                                    padding: EdgeInsets.only(top: 8),
                                    child: Row(
                                      children: [
                                        SizedBox(width: 12, height: 12, child: CircularProgressIndicator(strokeWidth: 2, color: Color(0xFFF59E0B))),
                                        SizedBox(width: 8),
                                        Text("Đang dịch...", style: TextStyle(color: Colors.white54, fontSize: 12, fontStyle: FontStyle.italic)),
                                      ],
                                    ),
                                  ),
                                if (_translatedOverview != null && widget.ep['_needs_translation'] == true)
                                  Padding(
                                    padding: const EdgeInsets.only(top: 8),
                                    child: Row(
                                      children: [
                                        const Icon(Icons.g_translate, color: Colors.white30, size: 14),
                                        const SizedBox(width: 6),
                                        Text(L10n.t('translated_by_google') ?? 'Dịch tự động bởi Google', style: const TextStyle(color: Colors.white30, fontSize: 12, fontStyle: FontStyle.italic)),
                                      ],
                                    ),
                                  ),
                              ],
                            ),"""
c = c.replace(full_overview_block, translated_block)

with open("lib/widgets/air_schedule_dialog.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Updated onTap and translation rendering")

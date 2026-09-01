import re

with open("lib/widgets/air_schedule_dialog.dart", "r", encoding="utf-8") as f:
    c = f.read()

# Add _showOriginal
c = c.replace("bool _isTranslating = false;", "bool _isTranslating = false;\n  bool _showOriginal = false;")

# Replace Text rendering
old_text = """                                Text(
                                  _translatedOverview ?? overview,
                                  style: const TextStyle(color: Colors.white70, fontSize: 14, height: 1.6),
                                ),"""

new_text = """                                Text(
                                  (_translatedOverview != null && !_showOriginal) ? _translatedOverview! : overview,
                                  style: const TextStyle(color: Colors.white70, fontSize: 14, height: 1.6),
                                ),"""
c = c.replace(old_text, new_text)

# Replace the row containing translated_by_google
old_row = """                                        const Icon(Icons.g_translate, color: Colors.white30, size: 14),
                                        const SizedBox(width: 6),
                                        Text(L10n.t('translated_by_google'), style: const TextStyle(color: Colors.white30, fontSize: 12, fontStyle: FontStyle.italic)),"""

new_row = """                                        const Icon(Icons.g_translate, color: Colors.white30, size: 14),
                                        const SizedBox(width: 6),
                                        Text(L10n.t('translated_by_google'), style: const TextStyle(color: Colors.white30, fontSize: 12, fontStyle: FontStyle.italic)),
                                        const Spacer(),
                                        GestureDetector(
                                          onTap: () {
                                            setState(() { _showOriginal = !_showOriginal; });
                                          },
                                          child: Text(
                                            _showOriginal ? L10n.t('show_translation') : L10n.t('show_original'),
                                            style: const TextStyle(color: Color(0xFFF59E0B), fontSize: 12, fontWeight: FontWeight.w500),
                                          ),
                                        ),"""
c = c.replace(old_row, new_row)

with open("lib/widgets/air_schedule_dialog.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Added show original toggle logic!")

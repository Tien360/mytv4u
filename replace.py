import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Replace RichText with SelectableText.rich in _buildRichText
text = re.sub(r'Widget _buildRichText\(String label, String value\) \{\s*return RichText\(', 'Widget _buildRichText(String label, String value) {\n    return SelectableText.rich(', text)

# Replace display name Text
text = re.sub(r'Text\(\s*_movie!\.displayName,', 'SelectableText(\n                                          _movie!.displayName,', text)

# Replace original name Text
text = re.sub(r'Text\(\s*_movie!\.originalName,', 'SelectableText(\n                                          _movie!.originalName,', text)

# Replace description Text
text = re.sub(r'Text\(\s*_movie!\.description\.replaceAll\(', 'SelectableText(\n                                          _movie!.description.replaceAll(', text)

# For actor name, we replace Text and remove overflow
# The original block is:
# Text(
#   actor['name'] ?? '',
#   style: const TextStyle(
#     color: Colors.white,
#     fontSize: 11,
#   ),
#   textAlign: TextAlign.center,
#   maxLines: 2,
#   overflow: TextOverflow.ellipsis,
# )

text = text.replace("Text(\n                                                          actor['name'] ?? '',\n                                                          style:\n                                                              const TextStyle(\n                                                                color: Colors\n                                                                    .white,\n                                                                fontSize: 11,\n                                                              ),\n                                                          textAlign:\n                                                              TextAlign.center,\n                                                          maxLines: 2,\n                                                          overflow: TextOverflow\n                                                              .ellipsis,\n                                                        )", "SelectableText(\n                                                          actor['name'] ?? '',\n                                                          style:\n                                                              const TextStyle(\n                                                                color: Colors\n                                                                    .white,\n                                                                fontSize: 11,\n                                                              ),\n                                                          textAlign:\n                                                              TextAlign.center,\n                                                          maxLines: 2,\n                                                        )")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)

print("Done")

import re

with open("lib/api/phim_api.dart", "r", encoding="utf-8") as f:
    content = f.read()

pattern = r"t = t\.replaceAll\(RegExp\(r'\(\?i\)\(.*?\)'\), ''\);"
replacement = r"t = t.replaceAll(RegExp(r'(vietsub|thuyết minh|lồng tiếng|bản đẹp|hd|fhd|4k|cam|ts|bluray|web-dl|tập \d+)', caseSensitive: false), '');"

# Instead of regex, just replace the line directly
content = content.replace("t = t.replaceAll(RegExp(r'(?i)(vietsub|thuyáº¿t minh|lá»“ng tiáº¿ng|báº£n Ä‘áº¹p|hd|fhd|4k|cam|ts|bluray|web-dl|táº­p \d+)'), '');", "t = t.replaceAll(RegExp(r'(vietsub|thuyết minh|lồng tiếng|bản đẹp|hd|fhd|4k|cam|ts|bluray|web-dl|tập \\d+)', caseSensitive: false), '');")

with open("lib/api/phim_api.dart", "w", encoding="utf-8") as f:
    f.write(content)

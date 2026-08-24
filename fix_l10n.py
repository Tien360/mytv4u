import re

with open("lib/utils/l10n.dart", "r", encoding="utf-8") as f:
    text = f.read()

new_method = """
  static List<String> tList(String key) {
    var val = _localizedStrings[key];
    if (val is List) {
      return val.map((e) => e.toString()).toList();
    }
    return [t(key)];
  }
}"""

text = re.sub(r'}\s*$', new_method, text)

with open("lib/utils/l10n.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated l10n.dart")

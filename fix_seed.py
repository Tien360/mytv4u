import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Replace random seed
text = text.replace("final random = DateTime.now().millisecondsSinceEpoch % phrases.length;", "final random = _phraseSeed % phrases.length;")

# Replace date formatting
old_date = "String fDate = L10n.currentLang == 'vi' ? '${airDate.day}/${airDate.month}/${airDate.year}' : airDateStr;"
new_date = """String getWeekday(int w) {
  if (L10n.currentLang == 'en') {
    const d = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    return d[w - 1];
  } else {
    return w == 7 ? 'CN' : 'T${w + 1}';
  }
}
String fDate = L10n.currentLang == 'vi' ? '(${getWeekday(airDate.weekday)} ${airDate.day}/${airDate.month}/${airDate.year})' : '(${getWeekday(airDate.weekday)} $airDateStr)';"""

text = text.replace(old_date, new_date)

# Replace next_info date formatting
old_next = """final estStr = L10n.currentLang == 'vi' ? '${estDate.day}/${estDate.month}/${estDate.year}' : '${estDate.year}-${estDate.month.toString().padLeft(2, '0')}-${estDate.day.toString().padLeft(2, '0')}';"""
new_next = """final estStr = L10n.currentLang == 'vi' ? '(${getWeekday(estDate.weekday)} ${estDate.day}/${estDate.month}/${estDate.year})' : '(${getWeekday(estDate.weekday)} ${estDate.year}-${estDate.month.toString().padLeft(2, '0')}-${estDate.day.toString().padLeft(2, '0')})';"""

text = text.replace(old_next, new_next)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Applied fixes")

import sys
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("import 'package:intl/intl.dart';", "")

target_format = """                                        final date = DateTime.parse(airDateStr);
                                        formattedDate = DateFormat('dd/MM/yyyy').format(date);"""
new_format = """                                        final date = DateTime.parse(airDateStr);
                                        formattedDate = '${date.day.toString().padLeft(2, '0')}/${date.month.toString().padLeft(2, '0')}/${date.year}';"""

if target_format in c:
    c = c.replace(target_format, new_format)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Removed intl")

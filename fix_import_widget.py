with open("lib/widgets/update_dialog.dart", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("import '../widgets/glass_container.dart';", "")

with open("lib/widgets/update_dialog.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Removed wrong import in update_dialog")

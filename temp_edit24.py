with open("lib/globals.dart", "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace("final ValueNotifier<bool> useTestDetailUi = ValueNotifier(true);", "")
with open("lib/globals.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Removed useTestDetailUi")

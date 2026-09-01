import re

with open("lib/widgets/air_schedule_dialog.dart", "r", encoding="utf-8") as f:
    c = f.read()

# find all const Text(L10n
c = re.sub(r"const\s+Text\(\s*L10n\.t", r"Text(L10n.t", c)
# also check if the whole padding or row is const
c = c.replace("const Padding(\n                                    padding: EdgeInsets.only(top: 8),\n                                    child: Row(\n                                      children: [\n                                        SizedBox(width: 12, height: 12, child: CircularProgressIndicator(strokeWidth: 2, color: Color(0xFFF59E0B))),\n                                        SizedBox(width: 8),\n                                        Text(L10n.t('translating'),",
              "Padding(\n                                    padding: const EdgeInsets.only(top: 8),\n                                    child: Row(\n                                      children: [\n                                        const SizedBox(width: 12, height: 12, child: CircularProgressIndicator(strokeWidth: 2, color: Color(0xFFF59E0B))),\n                                        const SizedBox(width: 8),\n                                        Text(L10n.t('translating'),")

with open("lib/widgets/air_schedule_dialog.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Fixed const issue")

with open("lib/main.dart", "r", encoding="utf-8") as f:
    c = f.read()

import_line = "import 'utils/l10n.dart';"
c = c.replace(import_line, import_line + "\nimport 'utils/location_helper.dart';")

init_line = "await initAmbientSettings();"
c = c.replace(init_line, init_line + "\n  LocationHelper.initUserCountry(); // Start fetching IP location in background")

with open("lib/main.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Updated main.dart!")

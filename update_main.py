import re

with open("lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

import_str = "import 'api/stremio_server.dart';"
new_import = "import 'api/stremio_server.dart';\nimport 'api/film4k_proxy.dart';"

content = content.replace(import_str, new_import)

init_str = "MediaKit.ensureInitialized();"
new_init = "MediaKit.ensureInitialized();\n  \n  // Khởi tạo proxy Film4k\n  Film4kProxy.start();"

content = content.replace(init_str, new_init)

with open("lib/main.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Added to main.dart")

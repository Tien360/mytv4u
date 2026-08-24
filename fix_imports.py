for file in ["lib/screens/library_screen.dart", "lib/screens/movie_detail_screen.dart", "lib/screens/splash_screen.dart", "lib/widgets/update_dialog.dart"]:
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Check if we need to add the import
    if "import '../widgets/glass_container.dart';" not in text:
        # Just put it at the top after package imports
        text = text.replace("import 'package:flutter/material.dart';", "import 'package:flutter/material.dart';\nimport '../widgets/glass_container.dart';")
        with open(file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Added GlassContainer import to {file}")

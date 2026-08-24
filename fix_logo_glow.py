import re

def update_logo_glow(file_path, is_detail):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Add dart:ui import if missing
    if "import 'dart:ui'" not in content and "import 'dart:ui' as ui;" not in content:
        content = content.replace("import 'package:flutter/material.dart';", "import 'package:flutter/material.dart';\nimport 'dart:ui' as ui;")

    # We want to replace the first Transform.translate inside the Stack of the logo
    if is_detail:
        var_name = "_tmdbLogoInfo"
    else:
        var_name = "logoInfo"
    
    # The stack is inside the Container which is inside if (logoInfo?.url != null)
    old_glow = """Transform.translate(
                                                          offset: const Offset(1, 1),
                                                          child: Image.network(
                                                            """ + var_name + """!.url!,
                                                            fit: BoxFit.contain,
                                                            alignment: Alignment.centerLeft,
                                                            color: Colors.white.withOpacity(0.5),
                                                            errorBuilder: (context, error, stackTrace) => const SizedBox(),
                                                          ),
                                                        ),"""
    
    new_glow = """ImageFiltered(
                                                          imageFilter: ui.ImageFilter.blur(sigmaX: 3.0, sigmaY: 3.0),
                                                          child: Image.network(
                                                            """ + var_name + """!.url!,
                                                            fit: BoxFit.contain,
                                                            alignment: Alignment.centerLeft,
                                                            color: Colors.white.withOpacity(0.7),
                                                            errorBuilder: (context, error, stackTrace) => const SizedBox(),
                                                          ),
                                                        ),"""
    
    content = content.replace(old_glow, new_glow)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

update_logo_glow("lib/screens/home_screen.dart", False)
update_logo_glow("lib/screens/movie_detail_screen.dart", True)

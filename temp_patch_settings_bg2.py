import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

bg_search = "      backgroundColor: Colors.transparent,"
bg_replace = "      backgroundColor: Colors.black,"
if bg_search in content:
    content = content.replace(bg_search, bg_replace)
    print("Reverted background color to black!")

import_search = "import 'package:flutter/material.dart';"
import_replace = "import 'package:flutter/material.dart';\nimport '../widgets/ambient_background.dart';"
if "ambient_background.dart" not in content:
    content = content.replace(import_search, import_replace)
    print("Added AmbientBackground import!")

stack_search = """      body: Stack(
        children: [
          SafeArea("""
stack_replace = """      body: Stack(
        children: [
          const AmbientBackground(),
          SafeArea("""
if "const AmbientBackground()" not in content:
    content = content.replace(stack_search, stack_replace)
    print("Added AmbientBackground to Stack!")

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

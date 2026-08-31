path = r"T:\Project\Phim\mytv4u_flutter\lib\widgets\audio_visualizer.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make it flexible
old_row = """    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.end,"""

new_row = """    return FittedBox(
      fit: BoxFit.scaleDown,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.end,"""

content = content.replace(old_row, new_row)
content = content.replace("    );\n  }\n}", "      ),\n    );\n  }\n}")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched AudioVisualizer with FittedBox")

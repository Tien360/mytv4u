import sys
with open('lib/widgets/fade_indexed_stack.dart', 'r', encoding='utf-8') as f:
    c = f.read()

target = """          child: TickerMode(
            enabled: isActive,
            child: IgnorePointer("""
new_target = """          child: TickerMode(
            enabled: shouldRender,
            child: IgnorePointer("""

if target in c:
    c = c.replace(target, new_target)
    print("Fixed TickerMode bug")
else:
    print("Target not found")

with open('lib/widgets/fade_indexed_stack.dart', 'w', encoding='utf-8') as f:
    f.write(c)

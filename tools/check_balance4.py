def check_balance(text):
    stack = []
    for i, c in enumerate(text):
        if c in '([{':
            stack.append((c, i))
        elif c in ')]}':
            if not stack:
                return
            top, pos = stack.pop()
            if text[:pos].count(chr(10))+1 == 349:
                print(f"The bracket from line 349 was popped by '{c}' at line {text[:i].count(chr(10))+1}")

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    check_balance(f.read())

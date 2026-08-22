def check_balance(text):
    stack = []
    for i, c in enumerate(text):
        if c in '([{':
            stack.append((c, i))
        elif c in ')]}':
            if not stack:
                return
            top, pos = stack.pop()
            if (c == ')' and top != '(') or (c == ']' and top != '[') or (c == '}' and top != '{'):
                print(f"Mismatch at index {i}, line {text[:i].count(chr(10))+1}: '{c}' found but expected to close '{top}' from line {text[:pos].count(chr(10))+1}")
                for s in stack:
                    print(f"Still open: {s[0]} at line {text[:s[1]].count(chr(10))+1}")
                return

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    check_balance(f.read())

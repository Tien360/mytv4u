def check_balance(text):
    stack = []
    for i, c in enumerate(text):
        if c in '([{':
            stack.append((c, i))
        elif c in ')]}':
            if not stack:
                print(f"Unmatched {c} at {i}")
                return
            top, _ = stack.pop()
            if (c == ')' and top != '(') or (c == ']' and top != '[') or (c == '}' and top != '{'):
                print(f"Mismatched {c} at {i}, expected match for {top}")
                return
    if stack:
        print(f"Unmatched {stack[-1][0]} at {stack[-1][1]}")

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    check_balance(f.read())

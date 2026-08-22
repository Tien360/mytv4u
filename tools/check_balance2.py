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
                print(f"Unclosed '{top}' at index {pos}, line {text[:pos].count(chr(10))+1}")
                print(text[pos-50:pos+50])
                return

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    check_balance(f.read())

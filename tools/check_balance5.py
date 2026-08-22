import sys
def check_balance(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    stack = []
    for i, c in enumerate(text):
        if c in '([{':
            stack.append((c, i))
        elif c in ')]}':
            if not stack:
                return
            top, pos = stack.pop()
            if (c == ')' and top != '(') or (c == ']' and top != '[') or (c == '}' and top != '{'):
                print(f"Unclosed '{top}' at index {pos}, line {text[:pos].count(chr(10))+1} before mismatched {c}")
                return

check_balance(sys.argv[1])

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()
import re
stack = []
for i, char in enumerate(text):
    if char in "([{":
        stack.append((char, i))
    elif char in ")]}":
        if not stack:
            print(f"Unmatched {char} at index {i}")
        else:
            top = stack.pop()
            if (char == ')' and top[0] != '(') or \
               (char == ']' and top[0] != '[') or \
               (char == '}' and top[0] != '{'):
                print(f"Mismatched {char} at index {i}. Expected match for {top[0]} at {top[1]}")
if stack:
    print(f"Unclosed braces: {stack}")
else:
    print("All braces matched!")

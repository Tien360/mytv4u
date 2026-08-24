with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()
import re
stack = []
for i, char in enumerate(text):
    if char in "([{":
        stack.append((char, i))
    elif char in ")]}":
        if not stack:
            print(f"Unmatched {char} at line {text[:i].count(chr(10))+1}")
        else:
            top = stack.pop()
            if (char == ')' and top[0] != '(') or \
               (char == ']' and top[0] != '[') or \
               (char == '}' and top[0] != '{'):
                print(f"Mismatched {char} at line {text[:i].count(chr(10))+1}. Expected match for {top[0]} at line {text[:top[1]].count(chr(10))+1}")

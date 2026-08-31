with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

stack = []
for i, line in enumerate(lines):
    for char in line:
        if char == '{':
            stack.append(i)
        elif char == '}':
            if stack:
                stack.pop()
            else:
                print(f"Unmatched }} at line {i+1}")

if stack:
    print(f"Unmatched {{ from line {stack[-1]+1}")
else:
    print("Braces matched perfectly!")

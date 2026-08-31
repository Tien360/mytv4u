with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

stack = []
class_start = -1
for i, line in enumerate(lines):
    if "class _MovieDetailScreenTestState" in line:
        class_start = len(stack) # wait, it's 0 usually
    
    for char in line:
        if char == '{':
            stack.append(i)
        elif char == '}':
            if stack:
                stack.pop()
                if len(stack) == class_start and class_start != -1:
                    print(f"Class closed at line {i+1}")
                    class_start = -1

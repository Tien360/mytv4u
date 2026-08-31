with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# I will find all '_mainScrollController.dispose();' and remove them.
c = c.replace("_mainScrollController.dispose();\n    super.dispose();", "super.dispose();")
c = c.replace("_mainScrollController.dispose();\r\n    super.dispose();", "super.dispose();")

# Then I will only add it to `_MovieDetailScreenTestState`'s dispose method
# Let's find `void dispose() {` inside `_MovieDetailScreenTestState`
start_class = c.find("class _MovieDetailScreenTestState")
if start_class != -1:
    end_class = c.find("class ", start_class + 50)
    if end_class == -1: end_class = len(c)
    
    block = c[start_class:end_class]
    block = block.replace("super.dispose();", "_mainScrollController.dispose();\n    super.dispose();", 1)
    
    c = c[:start_class] + block + c[end_class:]
    
    with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
        f.write(c)
    print("Fixed super.dispose")

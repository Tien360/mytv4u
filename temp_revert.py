with open("build_method.txt", "r", encoding="utf-16") as f:
    build_code = f.read()

with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    full_code = f.read()

b_start = full_code.find("  @override\n  Widget build(BuildContext context) {")
b_end = full_code.find("\n  Widget _buildBadgeIcon(", b_start)

if b_start != -1 and b_end != -1:
    full_code = full_code[:b_start] + build_code + full_code[b_end:]
    
    with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
        f.write(full_code)
    print("Reverted build method to .47")

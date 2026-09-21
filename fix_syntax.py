import re

with open("lib/api/phim_api.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Remove the incorrectly placed await ensureInit();
content = content.replace("    await ensureInit();\n    int page = 1,", "    int page = 1,")

# Put it correctly inside the function bodies!
old_body1 = """  }) async {
    String vsmovType = slug;"""
new_body1 = """  }) async {
    await ensureInit();
    String vsmovType = slug;"""
content = content.replace(old_body1, new_body1)

old_body2 = """  }) async {
    return _fetchAndMerge("""
new_body2 = """  }) async {
    await ensureInit();
    return _fetchAndMerge("""
content = content.replace(old_body2, new_body2)

with open("lib/api/phim_api.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed syntax")

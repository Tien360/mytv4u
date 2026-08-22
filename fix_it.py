with open("lib/api/phim_api.dart", "r", encoding="utf-8") as f:
    text = f.read()

index_start = text.find("images?api_key=import 'dart:async';")
if index_start != -1:
    index_start += len("images?api_key=")
    index_end = text.find("tmdbApiKey';\n        final res = await http.get(Uri.parse(imgUrl));", index_start)
    if index_end != -1:
        new_text = text[:index_start] + '$_' + text[index_end:]
        with open("lib/api/phim_api.dart", "w", encoding="utf-8") as f:
            f.write(new_text)
        print("Fixed phim_api.dart successfully")
    else:
        print("Could not find end marker")
else:
    print("Could not find start marker")

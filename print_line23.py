with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(1790, 1820):
    print(f"{i+1}: {lines[i].encode('ascii', 'ignore').decode('ascii').rstrip()}")

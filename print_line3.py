with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(2110, 2170):
    print(f"{i+1}: {lines[i].encode('ascii', 'ignore').decode('ascii').rstrip()}")

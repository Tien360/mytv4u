import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.readlines()
for i, l in enumerate(c):
    if "dispName =" in l:
        for x in range(max(0, i-5), min(i+10, len(c))):
            print(f"{x+1}: {c[x]}", end="")
        break

with open("orig.dart", "rb") as f:
    text = f.read().decode("utf-16", errors="ignore")
lines = text.split("\n")
for i, line in enumerate(lines):
    if "L10n.t('actors')" in line:
        for j in range(i+100, i+130):
            if j < len(lines):
                print(f"{j+1}: {lines[j].rstrip()}")
        break

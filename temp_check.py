with open("lib/widgets/air_schedule_dialog.dart", "r", encoding="utf-8") as f:
    for line in f:
        if "Tập" in line:
            print(line.strip())

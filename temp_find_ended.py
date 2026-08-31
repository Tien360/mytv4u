import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('T:/Project/Phim/tv_web_player/MainForm.cs', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("ended")
while idx != -1:
    print(content[idx-100:idx+150])
    idx = content.find("ended", idx+1)

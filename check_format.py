import os

folder = r"T:\Project\Phim\mytv4u_flutter\assets\easter\minions"
for filename in os.listdir(folder):
    path = os.path.join(folder, filename)
    with open(path, 'rb') as f:
        header = f.read(4)
        print(f"{filename}: {header}")

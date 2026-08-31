import os

folder = r"T:\Project\Phim\mytv4u_flutter\assets\easter\minions"
for filename in os.listdir(folder):
    path = os.path.join(folder, filename)
    with open(path, 'rb') as f:
        data = f.read(1024)
        is_apng = b'acTL' in data
        print(f"{filename} is APNG? {is_apng}")

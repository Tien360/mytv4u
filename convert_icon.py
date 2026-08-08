import sys
from PIL import Image

def convert(png_path, ico_path):
    img = Image.open(png_path)
    img.save(ico_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])

if __name__ == '__main__':
    convert(sys.argv[1], sys.argv[2])

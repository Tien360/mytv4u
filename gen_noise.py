import base64
import random
from PIL import Image

img = Image.new('L', (128, 128))
pixels = img.load()
for i in range(img.size[0]):
    for j in range(img.size[1]):
        pixels[i,j] = random.randint(0, 255)

img.save('noise.png')
with open('noise.png', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')
print("Base64 length:", len(b64))
with open('noise_b64.txt', 'w') as f:
    f.write(b64)

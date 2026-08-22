from PIL import Image, ImageDraw, ImageFont
import os

# Load app logo
logo_path = 'assets/logo.png'
if not os.path.exists(logo_path):
    print('Logo not found')
    exit(1)

app_logo = Image.open(logo_path).convert('RGBA')

# Create a 256x256 image
size = 256
img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
draw = ImageDraw.Draw(img)

# Draw a document/file shape
draw.rectangle([(32, 20), (224, 236)], fill=(240, 240, 245, 255), outline=(200, 200, 210, 255), width=8)
draw.polygon([(160, 20), (224, 20), (224, 84)], fill=(200, 200, 210, 255))

# Draw a music note in the center
draw.ellipse([(80, 140), (120, 170)], fill=(255, 50, 100, 255))
draw.rectangle([(110, 80), (120, 150)], fill=(255, 50, 100, 255))
draw.polygon([(110, 80), (170, 100), (170, 120), (120, 100)], fill=(255, 50, 100, 255))

# Overlay app logo in bottom right
logo_size = 96
app_logo = app_logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
img.paste(app_logo, (size - logo_size - 10, size - logo_size - 10), app_logo)

# Save as audio.ico
img.save('windows/runner/resources/audio.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
print('audio.ico generated')

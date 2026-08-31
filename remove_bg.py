from PIL import Image
import numpy as np

def remove_checkered_bg(img_path, out_path):
    img = Image.open(img_path).convert("RGBA")
    data = np.array(img)
    
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    
    # Checkered pattern is usually white (255) and light grey (around 204 or 240)
    # White background is (255, 255, 255)
    
    # Let's just make all pixels that are grayscale and very bright completely transparent.
    # To be safe, if R~=G~=B and R > 200, it's likely the background.
    
    is_bg = (abs(r.astype(int) - g.astype(int)) < 15) & (abs(g.astype(int) - b.astype(int)) < 15) & (r > 230)
    
    data[is_bg, 3] = 0  # set alpha to 0
    
    # For the checkered one, the grey squares might be like 240 or 230
    is_checkered_grey = (abs(r.astype(int) - g.astype(int)) < 15) & (abs(g.astype(int) - b.astype(int)) < 15) & (r > 200) & (r < 250)
    data[is_checkered_grey, 3] = 0
    
    Image.fromarray(data).save(out_path)

remove_checkered_bg(r'C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.user_uploaded\media_1788118538502.png', r'assets\images\music_icon.png')
remove_checkered_bg(r'C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.user_uploaded\media_1788118552351.png', r'assets\images\podcast_icon.png')

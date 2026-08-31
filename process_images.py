from PIL import Image
import os
import shutil

mic_src = r'C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.user_uploaded\media_1788124122433.png'
note_src = r'C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.user_uploaded\media_1788124141671.png'
mic_dst = r't:\Project\Phim\mytv4u_flutter\assets\images\podcast_icon.png'
note_dst = r't:\Project\Phim\mytv4u_flutter\assets\images\music_icon.png'

def make_transparent(img_path, out_path):
    try:
        img = Image.open(img_path).convert("RGBA")
        datas = img.getdata()
        newData = []
        for item in datas:
            # white or near white
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        img.save(out_path, "PNG")
        print(f"Processed {out_path}")
    except Exception as e:
        print(f"Error processing {img_path}: {e}")
        shutil.copy(img_path, out_path)

make_transparent(mic_src, mic_dst)
make_transparent(note_src, note_dst)


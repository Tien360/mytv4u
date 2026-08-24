from PIL import Image

def make_transparent(input_path, output_path):
    try:
        img = Image.open(input_path).convert("RGBA")
        datas = img.getdata()
        
        newData = []
        for item in datas:
            # white background: if RGB are all > 230, make transparent
            if item[0] > 235 and item[1] > 235 and item[2] > 235:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
                
        img.putdata(newData)
        img.save(output_path, "PNG")
        print(f"Made {output_path} transparent.")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

make_transparent("assets/easter/dynamite.jpg", "assets/easter/dynamite.png")
make_transparent("assets/easter/tissue.jpg", "assets/easter/tissue.png")
make_transparent("assets/easter/ufo.jpg", "assets/easter/ufo.png")
make_transparent("assets/easter/teddy.jpg", "assets/easter/teddy.png")

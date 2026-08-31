path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("height >= 2160", "height >= 4320")
content = content.replace("Phát nội dung 4K/8K yêu cầu phần cứng rất cao. Ứng dụng sẽ tự động chuyển sang trình phát MPV Toàn màn hình để tối ưu 100% sức mạnh GPU (Chống lag tuyệt đối).", "Phát nội dung 8K vô cùng nặng. Do cần tối ưu hệ thống triệt để, ứng dụng sẽ cần phát bằng trình phát MPV ngoài này để tận dụng 100% sức mạnh GPU (Chống lag tuyệt đối).")
content = content.replace("Chế độ UltraHD", "Chế độ 8K UltraHD")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated to 8K only")

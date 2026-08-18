import json
import os

def add_hello(file_path, hello_text):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data['hello'] = hello_text
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

add_hello('assets/langs/en.json', 'Hello')
add_hello('assets/langs/vi.json', 'Xin chào')
print("Fixed!")

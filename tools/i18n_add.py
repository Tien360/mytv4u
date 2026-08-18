import json
import sys

if len(sys.argv) < 4:
    print("Sử dụng: python tools/i18n_add.py <key_name> <vietnamese_text> <english_text>")
    print("Ví dụ: python tools/i18n_add.py new_button \"Nút mới\" \"New Button\"")
    sys.exit(1)

key = sys.argv[1]
vi_text = sys.argv[2]
en_text = sys.argv[3]

def add_to_json(filepath, k, v):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data[k] = v
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

add_to_json('assets/langs/vi.json', key, vi_text)
add_to_json('assets/langs/en.json', key, en_text)

print(f"Đã thêm thành công '{key}' vào cả vi.json và en.json!")
print(f"Bây giờ trong code, bạn chỉ cần dùng: L10n.t('{key}')")

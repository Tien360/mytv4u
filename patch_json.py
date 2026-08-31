import json

def update_lang(path, new_keys):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data.update(new_keys)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

vi_keys = {
  "yt_link_title": "Liên kết Tài khoản YouTube",
  "yt_linked_title": "Tài khoản YouTube đã liên kết",
  "yt_link_desc": "Sử dụng để xem các nội dung giới hạn độ tuổi và mở khóa chất lượng 4K/Premium.",
  "yt_linked_desc": "YouTube đã lưu cookie đăng nhập, bạn có thể xem video 4K/Premium và nội dung giới hạn độ tuổi.",
  "yt_login_btn": "Mở Trình duyệt Ẩn để Đăng nhập YouTube",
  "yt_unlink_btn": "Ngắt kết nối YouTube",
  "yt_unlink_msg": "Đã ngắt kết nối YouTube và hủy Cookie.",
  "yt_login_success": "Đăng nhập YouTube thành công! Cookie đã được lưu lại.",
  "yt_login_browser_title": "Trình duyệt Đăng nhập YouTube",
  "yt_login_browser_success": "Đăng nhập thành công, bạn có thể đóng cửa sổ này."
}

en_keys = {
  "yt_link_title": "Link YouTube Account",
  "yt_linked_title": "YouTube Account Linked",
  "yt_link_desc": "Use this to watch age-restricted content and unlock 4K/Premium qualities.",
  "yt_linked_desc": "YouTube has saved your login cookies. You can now watch 4K/Premium and age-restricted content.",
  "yt_login_btn": "Open Hidden Browser to Login",
  "yt_unlink_btn": "Unlink YouTube",
  "yt_unlink_msg": "Unlinked YouTube and cleared cookies.",
  "yt_login_success": "YouTube login successful! Cookies have been saved.",
  "yt_login_browser_title": "YouTube Login Browser",
  "yt_login_browser_success": "Login successful, you can now close this window."
}

update_lang("assets/langs/vi.json", vi_keys)
update_lang("assets/langs/en.json", en_keys)
print("Safely updated language JSONs")

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    "'Đăng nhập YouTube thành công! Cookie đã được lưu lại.'": "L10n.t('yt_login_success')",
    "'Trình duyệt Đăng nhập YouTube'": "L10n.t('yt_login_browser_title')",
    "'Đăng nhập thành công, bạn có thể đóng cửa sổ này.'": "L10n.t('yt_login_browser_success')",
    "_isYtLinked ? 'Tài khoản YouTube đã liên kết' : 'Liên kết Tài khoản YouTube'": "_isYtLinked ? L10n.t('yt_linked_title') : L10n.t('yt_link_title')",
    """_isYtLinked 
                        ? 'YouTube đã lưu cookie đăng nhập, bạn có thể xem video 4K/Premium và nội dung giới hạn độ tuổi.'
                        : 'Sử dụng để xem các nội dung giới hạn độ tuổi và mở khóa chất lượng 4K/Premium.'""": "_isYtLinked ? L10n.t('yt_linked_desc') : L10n.t('yt_link_desc')",
    "'Mở Trình duyệt Ẩn để Đăng nhập YouTube'": "L10n.t('yt_login_btn')",
    "'Ngắt kết nối YouTube'": "L10n.t('yt_unlink_btn')",
    "'Đã ngắt kết nối YouTube và hủy Cookie.'": "L10n.t('yt_unlink_msg')",
    # Also I have some weirdly encoded strings from earlier patches that I should match:
    "'Ä Äƒng nháº­p YouTube thÃ nh cÃ´ng! Cookie Ä‘Ã£ Ä‘Æ°á»£c lÆ°u láº¡i.'": "L10n.t('yt_login_success')",
    "'TrÃ¬nh duyá»‡t Ä Äƒng nháºp YouTube'": "L10n.t('yt_login_browser_title')",
    "'Ä Äƒng nháºp thÃnh cÃ´ng, báº¡n cÃ³ thá»ƒ Ä‘Ã³ng cá»a sá»• nÃy.'": "L10n.t('yt_login_browser_success')",
    "'Ä Ã£ ngáº¯t káº¿t ná»‘i YouTube vÃ  há»§y Cookie.'": "L10n.t('yt_unlink_msg')"
}

for k, v in replacements.items():
    content = content.replace(k, v)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated settings_screen.dart with L10n keys")

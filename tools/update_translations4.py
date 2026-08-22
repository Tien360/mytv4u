import json
import re
files = ['assets/langs/en.json', 'assets/langs/vi.json']
new_keys = {
    'en.json': {
        'return_public_version': 'Return to Public version ({version})',
        'beta_version': 'Beta version ({version})',
        'update_new_version': 'Update new version ({version})',
        'update_error': 'Error: {error}',
        'beta_warning': 'Warning: This is a beta version. It may contain bugs. Please backup your settings before installing.',
        'update_details': 'Update details:',
        'downloading_update': 'Downloading update...',
        'exit_app': 'Exit application'
    },
    'vi.json': {
        'return_public_version': 'Trở về phiên bản Public ({version})',
        'beta_version': 'Phiên bản thử nghiệm Beta ({version})',
        'update_new_version': 'Cập nhật phiên bản mới ({version})',
        'update_error': 'Lỗi: {error}',
        'beta_warning': 'Cảnh báo: Đây là phiên bản thử nghiệm (Beta). Có thể chứa một số lỗi. Hãy sao lưu cấu hình trước khi cài.',
        'update_details': 'Chi tiết bản cập nhật:',
        'downloading_update': 'Đang tải xuống bản cập nhật...',
        'exit_app': 'Thoát ứng dụng'
    }
}
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    filename = file.split('/')[-1]
    for k, v in new_keys[filename].items():
        if k not in data:
            data[k] = v
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

with open('lib/widgets/update_dialog.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("'Trở về phiên bản Public (${widget.updateInfo.latestVersion})'", "L10n.t('return_public_version', {'version': widget.updateInfo.latestVersion})")
content = content.replace("'Phiên bản thử nghiệm Beta (${widget.updateInfo.latestVersion})'", "L10n.t('beta_version', {'version': widget.updateInfo.latestVersion})")
content = content.replace("'Cập nhật phiên bản mới (${widget.updateInfo.latestVersion})'", "L10n.t('update_new_version', {'version': widget.updateInfo.latestVersion})")
content = content.replace("'Lỗi: $_error'", "L10n.t('update_error', {'error': _error})")
content = content.replace("'Cảnh báo: Đây là phiên bản thử nghiệm (Beta). Có thể chứa một số lỗi. Hãy sao lưu cấu hình trước khi cài.'", "L10n.t('beta_warning')")
content = content.replace("'Chi tiết bản cập nhật:'", "L10n.t('update_details')")
content = content.replace("'Đang tải xuống bản cập nhật...'", "L10n.t('downloading_update')")
content = content.replace("'Thoát ứng dụng'", "L10n.t('exit_app')")

with open('lib/widgets/update_dialog.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done update dialog')

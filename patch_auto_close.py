path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_code = """      if (!mounted) return;
      
      showDialog(
        context: context,"""

new_code = """      if (!mounted) return;
      
      bool isClosed = false;
      _controller.url.listen((url) {
        if (!isClosed && url.startsWith('https://www.youtube.com') && !url.contains('ServiceLogin')) {
           isClosed = true;
           _controller.dispose();
           Navigator.of(context, rootNavigator: true).pop();
           ScaffoldMessenger.of(context).showSnackBar(
             const SnackBar(
               content: Text('Đăng nhập YouTube thành công! Cookie đã được lưu lại.'),
               backgroundColor: Colors.green,
             ),
           );
        }
      });
      
      showDialog(
        context: context,"""

if "bool isClosed = false;" not in content:
    content = content.replace(old_code, new_code)
    
    # Also update the manual close button to set isClosed = true
    old_close = """                        onPressed: () {
                          _controller.dispose();
                          Navigator.pop(context);
                        },"""
    new_close = """                        onPressed: () {
                          isClosed = true;
                          _controller.dispose();
                          Navigator.pop(context);
                        },"""
    content = content.replace(old_close, new_close)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched auto-close logic")

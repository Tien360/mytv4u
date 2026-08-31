import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\library_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add _isLoadingUrl back
state_search = "bool _isLive = false;"
state_new = "bool _isLive = false;\n    bool _isLoadingUrl = false;"
if "bool _isLoadingUrl = false;" not in content:
    content = content.replace(state_search, state_new)

# 2. Add setState
btn_search = """onPressed: () async {
                        final url = _urlController.text.trim();
                        if (url.isNotEmpty) {"""
btn_new = """onPressed: () async {
                        final url = _urlController.text.trim();
                        if (url.isNotEmpty) {
                          setState(() { _isLoadingUrl = true; });"""
if "_isLoadingUrl = true;" not in content:
    content = content.replace(btn_search, btn_new)

# 3. Add UI loader
ui_search = """child: const Text('Mở', style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),"""
ui_new = """child: _isLoadingUrl 
                        ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                        : const Text('Mở', style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),"""
if "_isLoadingUrl \n" not in content and "? const SizedBox" not in content:
    content = content.replace(ui_search, ui_new)

# 4. Handle process retry
proc_search = """final res = await Process.run(exePath, args);
                              if (res.exitCode == 0) {"""
proc_new = """ProcessResult res = await Process.run(exePath, args);
                              if (res.exitCode != 0 && cookieSource != 'none') {
                                // Fallback
                                res = await Process.run(exePath, ['--dump-json', '--flat-playlist', url]);
                              }
                              
                              if (res.exitCode == 0) {"""
if "ProcessResult res = await Process.run" not in content:
    content = content.replace(proc_search, proc_new)

# 5. Fix finally state
end_search = """                          if (mounted) {
                            
                            Navigator.pop(context);"""
end_new = """                          if (mounted) {
                            setState(() { _isLoadingUrl = false; });
                            Navigator.pop(context);"""
if "_isLoadingUrl = false;" not in content:
    content = content.replace(end_search, end_new)


with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed library_screen.dart")

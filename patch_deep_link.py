path = r"T:\Project\Phim\mytv4u_flutter\lib\services\deep_link_service.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_str = """        await Process.run('cmd', [
          '/c',
          'reg',
          'add',
          'HKCU\\\\Software\\\\Classes\\\\$audioProgId\\\\DefaultIcon',
          '/ve',
          '/d',
          '"$audioIcoPath"',
          '/f',
        ]);"""
        
new_str = """        await Process.run('cmd', [
          '/c',
          'reg',
          'add',
          'HKCU\\\\Software\\\\Classes\\\\$audioProgId\\\\DefaultIcon',
          '/ve',
          '/d',
          '"$exePath",1',
          '/f',
        ]);"""

if old_str in content:
    content = content.replace(old_str, new_str)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched deep_link_service.dart for audio icon index")
else:
    print("Could not find old_str")

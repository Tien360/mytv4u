with open('lib/api/phim_api.dart', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('static String _processM3u8Url(String url) {')
end_idx = text.find('return url;\n    }', start_idx) + len('return url;\n    }')

old_func = text[start_idx:end_idx]

new_func = '''static String _processM3u8Url(String url) {
    if (url.isEmpty) return url;
    if (url.contains('workers.dev') ||
        (url.contains('dpdns.org') && !url.contains('stream/hls'))) {
      final rawId = url.split('/').last;
      return 'premium://play/';
    }
    return url;
  }'''

if start_idx != -1:
    new_text = text[:start_idx] + new_func + text[end_idx:]
    with open('lib/api/phim_api.dart', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('Patched successfully')
else:
    print('Function not found!')

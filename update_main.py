import re

with open('lib/screens/main_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the sidebar label from nav_favorite to Thư viện
content = re.sub(r"_buildNavItem\(Icons\.favorite_outline, Icons\.favorite, L10n\.t\('nav_favorite'\) \?\? 'Yêu thích', 5\)", 
                 r"_buildNavItem(Icons.folder_outlined, Icons.folder, L10n.t('nav_favorite') != null ? 'Thư viện & Yêu thích' : 'Thư viện & Yêu thích', 5)", 
                 content)
content = re.sub(r"_buildNavItem\(Icons\.favorite_outline, Icons\.favorite, L10n\.t\('nav_favorite'\), 5\)",
                 r"_buildNavItem(Icons.folder_outlined, Icons.folder, 'Thư viện', 5)", 
                 content)

# 2. Add speech_to_text import
if 'speech_to_text' not in content:
    content = "import 'package:speech_to_text/speech_to_text.dart' as stt;\n" + content

# 3. Add speech state variables
if '_speech' not in content:
    content = content.replace('bool _isSidebarCollapsed = false;', 'bool _isSidebarCollapsed = false;\n  late stt.SpeechToText _speech;\n  bool _isListening = false;')
    content = content.replace('super.initState();', 'super.initState();\n    _speech = stt.SpeechToText();')
    
    listen_func = '''
  void _listen() async {
    if (!_isListening) {
      bool available = await _speech.initialize(
        onStatus: (val) {
          if (val == 'done' || val == 'notListening') {
            if (mounted) setState(() => _isListening = false);
            if (_searchController.text.isNotEmpty) {
              if (_selectedIndex == 3) _tvKey.currentState?.performSearch(_searchController.text);
              else if (_selectedIndex == 4) _sportKey.currentState?.performSearch(_searchController.text);
              else _searchKey.currentState?.performSearch(_searchController.text);
            }
          }
        },
        onError: (val) => print('onError: '),
      );
      if (available) {
        setState(() => _isListening = true);
        String locale = L10n.currentLang == 'vi' ? 'vi_VN' : 'en_US';
        _speech.listen(
          localeId: locale,
          onResult: (val) => setState(() {
            _searchController.text = val.recognizedWords;
          }),
        );
      }
    } else {
      setState(() => _isListening = false);
      _speech.stop();
      if (_searchController.text.isNotEmpty) {
        if (_selectedIndex == 3) _tvKey.currentState?.performSearch(_searchController.text);
        else if (_selectedIndex == 4) _sportKey.currentState?.performSearch(_searchController.text);
        else _searchKey.currentState?.performSearch(_searchController.text);
      }
    }
  }

  Key _stackKey = UniqueKey();
'''
    content = content.replace('Key _stackKey = UniqueKey();', listen_func)

# 4. Add mic button to search bar
# We find the IconButton for clear and append the Mic button.
search_bar_end = r'''
                      IconButton(
                        icon: const Icon(Icons.clear, color: Colors.white54, size: 18),
                        onPressed: () {
                          _searchController.clear();
                          setState(() {});
                          if (_selectedIndex == 3) {
                            _tvKey.currentState?.performSearch('');
                          } else if (_selectedIndex == 4) {
                            _sportKey.currentState?.performSearch('');
                          } else if (_selectedIndex == 2) {
                            _searchKey.currentState?.performSearch('');
                          }
                        },
                      ),
'''
mic_button = r'''
                      IconButton(
                        icon: Icon(
                          _isListening ? Icons.mic : Icons.mic_none,
                          color: _isListening ? Colors.redAccent : Colors.white54,
                          size: 18
                        ),
                        onPressed: _listen,
                        tooltip: 'Tìm kiếm bằng giọng nói',
                      ),
'''
if 'Tìm kiếm bằng giọng nói' not in content:
    content = content.replace(search_bar_end, search_bar_end + mic_button)


with open('lib/screens/main_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated main_screen.dart')

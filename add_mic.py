import re
with open('lib/screens/main_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the closing parenthesis of Expanded(child: TextField(...)) to also append the mic button
mic_btn = '''
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

content = re.sub(r'if \(_searchController\.text\.isNotEmpty\)\s*IconButton\([\s\S]*?\}\s*,\s*\),', r'\g<0>\n' + mic_btn, content)

with open('lib/screens/main_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Added mic button!")

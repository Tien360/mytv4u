import sys

with open('lib/screens/game_detail_screen.dart', 'r', encoding='utf-8') as f:
    c = f.read()

# Remove the confusing Firebase login requirement
target_button = """                  if (_currentUser == null)
                    MouseRegion(
                      cursor: SystemMouseCursors.click,
                      child: GestureDetector(
                        onTap: () async {
                          final user = await AuthApi.loginWithGoogle();
                          if (user != null) {
                            setState(() => _currentUser = user);
                            _onPlayTap();
                          }
                        },
                        child: _buildPlayButton('ĐĂNG NHẬP GOOGLE & CHƠI', true),
                      ),
                    )
                  else
                    MouseRegion(
                      cursor: SystemMouseCursors.click,
                      child: GestureDetector(
                        onTap: _onPlayTap,
                        child: _buildPlayButton('▶ CHƠI NGAY', false),
                      ),
                    ),"""

new_button = """                  MouseRegion(
                    cursor: SystemMouseCursors.click,
                    child: GestureDetector(
                      onTap: _onPlayTap,
                      child: _buildPlayButton('▶ CHƠI NGAY', false),
                    ),
                  ),"""

if target_button in c:
    c = c.replace(target_button, new_button)
    print("Fixed Play Button")
else:
    print("Could not find Play Button. Let's try alternative.")
    # Maybe it uses ElevatedButton?
    
    target2 = """                  if (_currentUser == null)
                    ElevatedButton(
                      onPressed: () async {
                        final user = await AuthApi.loginWithGoogle();
                        if (user != null) {
                          setState(() => _currentUser = user);
                          _onPlayTap();
                        }
                      },
                      child: const Text('ĐĂNG NHẬP GOOGLE & CHƠI'),
                    )
                  else
                    ElevatedButton(
                      onPressed: _onPlayTap,
                      child: const Text('▶ CHƠI NGAY'),
                    )"""
    new_target2 = """                  ElevatedButton(
                    onPressed: _onPlayTap,
                    child: const Text('▶ CHƠI NGAY'),
                  )"""
    if target2 in c:
        c = c.replace(target2, new_target2)
        print("Fixed Play Button (alternative)")

with open('lib/screens/game_detail_screen.dart', 'w', encoding='utf-8') as f:
    f.write(c)


import re

with open('lib/screens/movie_detail_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

target = """                                      children: [
                                        SelectableText(
                                          _movie!.displayName,
                                          style: const TextStyle(
                                            fontSize: 48,
                                            fontWeight: FontWeight.bold,
                                            color: Colors.white,
                                            height: 1.1,
                                            shadows: [
                                              Shadow(
                                                color: Colors.black,
                                                blurRadius: 10,
                                              ),
                                            ],
                                          ),
                                        ),"""

replacement = """                                      children: [
                                        if (_movieLogo != null)
                                          Container(
                                            constraints: const BoxConstraints(maxHeight: 120, maxWidth: 500),
                                            alignment: Alignment.centerLeft,
                                            child: Image.network(
                                              _movieLogo!,
                                              fit: BoxFit.contain,
                                              alignment: Alignment.centerLeft,
                                              errorBuilder: (context, error, stackTrace) {
                                                return SelectableText(
                                                  _movie!.displayName,
                                                  style: const TextStyle(
                                                    fontSize: 48,
                                                    fontWeight: FontWeight.bold,
                                                    color: Colors.white,
                                                    height: 1.1,
                                                    shadows: [
                                                      Shadow(
                                                        color: Colors.black,
                                                        blurRadius: 10,
                                                      ),
                                                    ],
                                                  ),
                                                );
                                              },
                                            ),
                                          )
                                        else
                                          SelectableText(
                                            _movie!.displayName,
                                            style: const TextStyle(
                                              fontSize: 48,
                                              fontWeight: FontWeight.bold,
                                              color: Colors.white,
                                              height: 1.1,
                                              shadows: [
                                                Shadow(
                                                  color: Colors.black,
                                                  blurRadius: 10,
                                                ),
                                              ],
                                            ),
                                          ),"""

new_content = content.replace(target, replacement)
if new_content != content:
    with open('lib/screens/movie_detail_screen.dart', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Replaced!")
else:
    print("Not found!")

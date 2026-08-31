import re

path = r"T:\Project\Phim\tv_web_player\MainForm.cs"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r"style\.innerHTML = \s*\.nav-menu, \.now-playing, \.last-update, \.group-title, \.channel-grid, \.search-container, \.footer \{ display: none !important; \}\s*body, html, \.container, \.player-wrapper, \.video-box \{ \s*margin: 0 !important; \s*padding: 0 !important; \s*max-width: 100% !important; \s*width: 100vw !important; \s*height: 100vh !important; \s*border-radius: 0 !important; \s*\}\s*;"

new_css = """style.innerHTML = `
                        header, footer, nav, .nav-menu, .now-playing, .last-update, .group-title, .channel-grid, .search-container, .footer, .ads, [class*='header'], [class*='footer'], .sidebar { display: none !important; opacity: 0 !important; pointer-events: none !important; }
                        body, html { margin: 0 !important; padding: 0 !important; overflow: hidden !important; background: #000 !important; }
                        .container, .player-wrapper, .video-box, #player, .jwplayer { 
                            position: fixed !important;
                            top: 0 !important;
                            left: 0 !important;
                            margin: 0 !important; 
                            padding: 0 !important; 
                            max-width: 100% !important; 
                            width: 100vw !important; 
                            height: 100vh !important; 
                            border-radius: 0 !important; 
                            z-index: 99999 !important;
                        }
                    `;"""

content = re.sub(pattern, new_css, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done patching CSS syntax error in MainForm.cs")

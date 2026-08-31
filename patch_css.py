import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\youtube_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern_css = r"html, body, ytd-app, #background\.ytd-app, ytd-page-manager \{[\s\S]*?\}"
repl_css = """html, body, ytd-app, ytd-page-manager, #background, #page-manager {
          background: transparent !important;
          background-color: transparent !important;
        }
        html[dark], html {
          --yt-spec-base-background: transparent !important;
          --yt-spec-brand-background-solid: transparent !important;
          --yt-spec-brand-background-primary: transparent !important;
          --yt-spec-general-background-a: transparent !important;
          --yt-spec-general-background-b: transparent !important;
          --yt-spec-general-background-c: transparent !important;
          --yt-spec-menu-background: rgba(30,30,30,0.8) !important;
        }"""
content = re.sub(pattern_css, repl_css, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated CSS in youtube_screen.dart")

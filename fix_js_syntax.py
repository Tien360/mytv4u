import re
path = r"T:\Project\Phim\tv_web_player\MainForm.cs"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_block = """                    if (document.body) observer.observe(document.body, { childList: true, subtree: true });
                })();
            ";"""

good_block = """                    });
                    if (document.body) observer.observe(document.body, { childList: true, subtree: true });
                })();
            ";"""

content = content.replace(bad_block, good_block)

# Let me also check if the WebResourceRequested filter is what broke the compiler
# Wait, look at line 630: `let skipBtn = document.querySelector('.jw-skip, .jw-skip-ad, .vast-skip-button, [class*="skip"], [class*="Skip"], .videoAdUiSkipButton');`
# I used double quotes inside `[class*="skip"]`.
# But `jsAdBlocker` is defined with `@"..."`. In C# verbatim strings, double quotes MUST be escaped as `""`.
# So `[class*="skip"]` -> `[class*=""skip""]`
content = content.replace('[class*="skip"]', '[class*=""skip""]')
content = content.replace('[class*="Skip"]', '[class*=""Skip""]')
content = content.replace('[class*="-ad-"]', '[class*=""-ad-""]')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed missing braces and double quotes")

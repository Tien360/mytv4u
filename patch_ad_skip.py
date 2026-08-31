import re

path = r"T:\Project\Phim\tv_web_player\MainForm.cs"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_js = """                    if (document.body) observer.observe(document.body, { childList: true, subtree: true });
                })();
            ";"""

good_js = """                    if (document.body) observer.observe(document.body, { childList: true, subtree: true });
                    
                    // Force ad skip via interval for persistent VAST/VPAID players
                    setInterval(function() {
                        var els = document.querySelectorAll('div, button, a, span');
                        for(var i = 0; i < els.length; i++) {
                            var txt = els[i].innerText || '';
                            if (txt.toLowerCase().includes('bỏ qua quảng cáo') || txt.toLowerCase().includes('skip ad')) {
                                try { els[i].click(); } catch(e){}
                            }
                        }
                        let skipBtn = document.querySelector('.jw-skip, .jw-skip-ad, .vast-skip-button, [class*=""skip""], [class*=""Skip""], .videoAdUiSkipButton');
                        if (skipBtn) {
                            try { skipBtn.click(); } catch(e){}
                        }
                    }, 500);
                })();
            ";"""

content = content.replace(bad_js, good_js)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated MainForm.cs with aggressive skip ad interval.")

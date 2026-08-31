import re

path = r"T:\Project\Phim\tv_web_player\MainForm.cs"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_str = """                    // Force ad skip via interval for persistent VAST/VPAID players
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
                })();"""

new_str = """                    // Force ad skip via interval for persistent VAST/VPAID players
                    setInterval(function() {
                        var els = document.querySelectorAll('div, button, a, span');
                        var isAdPlaying = false;
                        for(var i = 0; i < els.length; i++) {
                            var txt = els[i].innerText || '';
                            if (txt.toLowerCase().includes('bỏ qua quảng cáo') || txt.toLowerCase().includes('skip ad')) {
                                try { els[i].click(); } catch(e){}
                            }
                            if (txt.toLowerCase().includes('quảng cáo sẽ đóng') || txt.toLowerCase().includes('giây') && txt.toLowerCase().includes('quảng cáo')) {
                                isAdPlaying = true;
                            }
                        }
                        let skipBtn = document.querySelector('.jw-skip, .jw-skip-ad, .vast-skip-button, [class*=""skip""], [class*=""Skip""], .videoAdUiSkipButton');
                        if (skipBtn) {
                            try { skipBtn.click(); } catch(e){}
                        }
                        if (document.querySelector('.jw-ad, .jw-ad-playing, [class*=""jw-ad""]')) {
                            isAdPlaying = true;
                        }
                        try {
                            if (window.jwplayer && typeof window.jwplayer === 'function') {
                                var jw = window.jwplayer();
                                if (jw && typeof jw.skipAd === 'function') {
                                    jw.skipAd();
                                }
                            }
                        } catch(e) {}

                        if (isAdPlaying) {
                            let vid = document.querySelector('video');
                            if (vid && !vid.paused && vid.duration && vid.currentTime < vid.duration) {
                                // Tua tới sát cuối quảng cáo để ép nó kết thúc
                                vid.currentTime = vid.duration - 0.1;
                                try { vid.play(); } catch(e){}
                            }
                        }
                    }, 150);
                })();"""

if old_str in content:
    content = content.replace(old_str, new_str)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced C# adblocker")
else:
    print("Could not find exact JS block.")

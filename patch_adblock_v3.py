import re

path = r"T:\Project\Phim\tv_web_player\MainForm.cs"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r"setInterval\(function\(\) \{.*?(?=\}\(\)\;\s+\"\;)", re.DOTALL)

good_js = """setInterval(function() {
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
                            if (vid && !vid.paused && vid.duration) {
                                // Tua tới sát cuối quảng cáo để ép nó kết thúc
                                vid.currentTime = vid.duration - 0.1;
                            }
                        }
                    }, 300);
                """

if pattern.search(content):
    content = pattern.sub(good_js, content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated JS AdBlocker successfully.")
else:
    print("Failed to find JS AdBlocker interval to replace.")

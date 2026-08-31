import re
import os

path = r"T:\Project\Phim\tv_web_player\MainForm.cs"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add auto-clicker for skip buttons
new_observer = """var observer = new MutationObserver(function(mutations) {
                        mutations.forEach(function(m) {
                            m.addedNodes.forEach(function(n) {
                                if (n.tagName === 'IFRAME' || n.tagName === 'A' || n.tagName === 'DIV') {
                                    if (n.className && typeof n.className === 'string' && n.className.includes('ad')) {
                                        n.style.display = 'none';
                                    }
                                }
                            });
                        });
                        
                        // Auto-skip ad buttons
                        let skipBtn = document.querySelector('.jw-skip, .jw-skip-ad, .vast-skip-button, [class*="skip"], [class*="Skip"], .videoAdUiSkipButton');
                        if (skipBtn) {
                            try { skipBtn.click(); } catch(e){}
                        }
                        
                        // Fast forward ad if it's forced
                        let video = document.querySelector('video');
                        let adContainer = document.querySelector('.jw-ad, .ad-container, [class*="-ad-"]');
                        if (video && adContainer && window.getComputedStyle(adContainer).display !== 'none') {
                           if (!video.paused) {
                               video.currentTime = video.duration || 999;
                           }
                        }
                    });"""

content = re.sub(r"var observer = new MutationObserver\(function\(mutations\).*?\n.*?\}\);", new_observer, content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated jsAdBlocker in MainForm.cs")

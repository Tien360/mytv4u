using System;
using System.IO;
using System.Text.RegularExpressions;

class Program {
    static void Main() {
        string path = @"T:\Project\Phim\tv_web_player\MainForm.cs";
        string content = File.ReadAllText(path);
        
        string oldCss = @"style.innerHTML = 
                        .nav-menu, .now-playing, .last-update, .group-title, .channel-grid, .search-container, .footer { display: none !important; }
                        body, html, .container, .player-wrapper, .video-box { 
                            margin: 0 !important; 
                            padding: 0 !important; 
                            max-width: 100% !important; 
                            width: 100vw !important; 
                            height: 100vh !important; 
                            border-radius: 0 !important; 
                        }
                    ;";

        string newCss = @"style.innerHTML = `
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
                    `;";

        content = content.Replace(oldCss, newCss);

        // Also fix the flex divs logic to hide the channel navigation
        string oldFlex = @"var flexDivs = document.querySelectorAll('div[style*=""display: flex""]');
                    flexDivs.forEach(d => {
                        if(d.innerHTML.includes('Knh Tru?c') || d.innerHTML.includes('nav-btn')) d.style.display = 'none';
                    });";
        string newFlex = @"var allDivs = document.querySelectorAll('div');
                    allDivs.forEach(d => {
                        if(d.innerHTML && (d.innerHTML.includes('Kênh Trước') || d.innerHTML.includes('Kênh Sau') || d.innerHTML.includes('Quốc Tế'))) {
                            d.style.display = 'none';
                        }
                    });";
        content = content.Replace(oldFlex, newFlex);

        File.WriteAllText(path, content);
        Console.WriteLine("Done patching CSS syntax error in MainForm.cs");
    }
}

using System;
using System.IO;

class Program {
    static void Main() {
        string path = @"T:\Project\Phim\tv_web_player\MainForm.cs";
        string content = File.ReadAllText(path);
        
        string injectionCode = @"
            string tvCleanupJs = @""
                try {
                    var style = document.createElement('style');
                    style.innerHTML = `
                        .nav-menu, .now-playing, .last-update, .group-title, .channel-grid, .search-container, .footer { display: none !important; }
                        body, html, .container, .player-wrapper, .video-box { 
                            margin: 0 !important; 
                            padding: 0 !important; 
                            max-width: 100% !important; 
                            width: 100vw !important; 
                            height: 100vh !important; 
                            border-radius: 0 !important; 
                        }
                    `;
                    document.head.appendChild(style);
                    
                    var flexDivs = document.querySelectorAll('div[style*=""display: flex""]');
                    flexDivs.forEach(d => {
                        if(d.innerHTML.includes('Kênh Trước') || d.innerHTML.includes('nav-btn')) d.style.display = 'none';
                    });
                } catch(e) {}
            "";
            await webView.CoreWebView2.ExecuteScriptAsync(tvCleanupJs);
";

        if (!content.Contains("var flexDivs = document.querySelectorAll")) {
            content = content.Replace("await InjectOverlayUI();", injectionCode + "\n            await InjectOverlayUI();");
            File.WriteAllText(path, content);
            Console.WriteLine("Injected TV cleanup JS into MainForm.cs");
        } else {
            Console.WriteLine("Already injected.");
        }
    }
}

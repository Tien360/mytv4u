import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('T:/Project/Phim/tv_web_player/MainForm.cs', 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = """                // Block Ads at Network Level
                webView.CoreWebView2.AddWebResourceRequestedFilter("*vast*", Microsoft.Web.WebView2.Core.CoreWebView2WebResourceContext.All);
                webView.CoreWebView2.AddWebResourceRequestedFilter("*vmap*", Microsoft.Web.WebView2.Core.CoreWebView2WebResourceContext.All);
                webView.CoreWebView2.AddWebResourceRequestedFilter("*adserver*", Microsoft.Web.WebView2.Core.CoreWebView2WebResourceContext.All);
                webView.CoreWebView2.AddWebResourceRequestedFilter("*doubleclick.net*", Microsoft.Web.WebView2.Core.CoreWebView2WebResourceContext.All);
                webView.CoreWebView2.AddWebResourceRequestedFilter("*googleads*", Microsoft.Web.WebView2.Core.CoreWebView2WebResourceContext.All);
                webView.CoreWebView2.AddWebResourceRequestedFilter("*ads*", Microsoft.Web.WebView2.Core.CoreWebView2WebResourceContext.All); // Broad but effective for ad network scripts

                webView.CoreWebView2.WebResourceRequested += (s, e) =>
                {
                    // If it's a known ad tracking or VAST xml, block it
                    e.Response = webView.CoreWebView2.Environment.CreateWebResourceResponse(
                        new System.IO.MemoryStream(), 403, "Blocked by AdBlock", "Content-Type: text/plain"
                    );
                };"""

new_logic = """                // Removed network-level AdBlock due to NguonC's Anti-Adblock detection.
                // We will rely purely on CSS hiding (jsAdBlocker) to avoid triggering the detector."""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open('T:/Project/Phim/tv_web_player/MainForm.cs', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Disabled network adblock in tv_web_player")
else:
    print("Could not find old_logic")

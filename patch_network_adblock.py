import re

path = r"T:\Project\Phim\tv_web_player\MainForm.cs"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

filter_code = """
                await webView.EnsureCoreWebView2Async(env);
                
                // Block Ads at Network Level
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
                };
"""

content = re.sub(r"await webView\.EnsureCoreWebView2Async\(env\);", filter_code, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Injected WebView2 WebResourceRequested Filter")

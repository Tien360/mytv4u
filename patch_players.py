import re

def patch_player(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Patch PremiumResolver intercept to ONLY trigger for premium://
    old_premium = """    if (_currentUrl.startsWith('premium://') || _currentUrl.contains('workers.dev') || _currentUrl.contains('dpdns.org')) {"""
    new_premium = """    if (_currentUrl.startsWith('premium://')) {"""
    content = content.replace(old_premium, new_premium)
    
    # 2. Patch _tryFallbackDomain
    old_fallback = """    if (_currentUrl.contains('dpdns.org') ||
        _currentUrl.contains('workers.dev') ||
        _currentUrl.contains('railway.app') ||
        _currentUrl.startsWith('premium://')) {"""
    
    new_fallback = """    if ((_currentUrl.contains('dpdns.org') && !_currentUrl.contains('stream/hls')) ||
        (_currentUrl.contains('workers.dev') && !_currentUrl.contains('stream/hls')) ||
        _currentUrl.contains('railway.app') ||
        _currentUrl.startsWith('premium://')) {"""
        
    content = content.replace(old_fallback, new_fallback)

    # Note: the spaces in _tryFallbackDomain might be slightly different. Let's use regex for fallback
    pattern = r"if\s*\(_currentUrl\.contains\('dpdns\.org'\)\s*\|\|\s*_currentUrl\.contains\('workers\.dev'\)\s*\|\|\s*_currentUrl\.contains\('railway\.app'\)\s*\|\|\s*_currentUrl\.startsWith\('premium://'\)\)\s*\{"
    
    replacement = """if ((_currentUrl.contains('dpdns.org') && !_currentUrl.contains('stream/hls')) ||
        (_currentUrl.contains('workers.dev') && !_currentUrl.contains('stream/hls')) ||
        _currentUrl.contains('railway.app') ||
        _currentUrl.startsWith('premium://')) {"""
        
    content = re.sub(pattern, replacement, content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

patch_player("lib/screens/player_screen.dart")
patch_player("lib/screens/yt_player_screen.dart")
print("Patched players")

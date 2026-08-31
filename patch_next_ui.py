import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

search = """  Widget _buildNextEpisodeOverlay() {
    bool hasNext = _currentIndex + 1 < widget.episodes.length;
    int remaining = _duration.inSeconds - _position.inSeconds;

    return Container(
      decoration: BoxDecoration(
        color: Colors.black.withOpacity(0.8),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.white24, width: 1),
      ),
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                hasNext
                    ? 'T?p ti?p theo s? pht sau $remaining giy'
                    : 'Phim s? dng sau $remaining giy',
                style: const TextStyle(color: Colors.white70, fontSize: 14),
              ),
              const SizedBox(height: 4),
              Text(
                hasNext
                    ? widget.episodes[_currentIndex + 1].name
                    : L10n.t('finished') ?? 'K?t thc',
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),"""

# Let's do a regex replacement because of unicode characters (Tập tiếp theo)
search_regex = r"Widget _buildNextEpisodeOverlay\(\) \{.*?(?=const SizedBox\(width: 24\),)"
new_logic = """Widget _buildNextEpisodeOverlay() {
    bool hasNext = _currentIndex + 1 < widget.episodes.length;
    int remaining = _duration.inSeconds - _position.inSeconds;
    
    bool hasThumb = false;
    String thumbUrl = '';
    if (hasNext) {
      final nextEp = widget.episodes[_currentIndex + 1];
      if (nextEp.embedUrl.contains('ytimg.com')) {
        hasThumb = true;
        thumbUrl = nextEp.embedUrl.replaceAll('maxresdefault', 'mqdefault');
      }
    }

    return Container(
      decoration: BoxDecoration(
        color: Colors.black.withOpacity(0.8),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.white24, width: 1),
      ),
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (hasThumb) ...[
            ClipRRect(
              borderRadius: BorderRadius.circular(6),
              child: Image.network(
                thumbUrl, 
                width: 100, 
                height: 56, 
                fit: BoxFit.cover,
                errorBuilder: (c,e,s) => Container(width: 100, height: 56, color: Colors.grey[900]),
              ),
            ),
            const SizedBox(width: 16),
          ],
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                hasNext
                    ? 'Tập tiếp theo sẽ phát sau $remaining giây'
                    : 'Phim sẽ đóng sau $remaining giây',
                style: const TextStyle(color: Colors.white70, fontSize: 14),
              ),
              const SizedBox(height: 4),
              SizedBox(
                width: 250,
                child: Text(
                  hasNext
                      ? widget.episodes[_currentIndex + 1].name
                      : L10n.t('finished') ?? 'Kết thúc',
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
"""

import re
content = re.sub(search_regex, new_logic, content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched Next Episode overlay successfully.")

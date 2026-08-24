import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Helper function to translate TMDB Status
status_translator = """
  String _translateStatus(String status) {
    if (L10n.currentLang == 'en') return status;
    switch (status) {
      case 'Released':
        return 'Đã phát hành';
      case 'Returning Series':
        return 'Đang phát sóng';
      case 'Ended':
        return 'Đã kết thúc';
      case 'Canceled':
        return 'Đã hủy';
      case 'In Production':
        return 'Đang sản xuất';
      case 'Planned':
        return 'Đã lên kế hoạch';
      case 'Rumored':
        return 'Tin đồn';
      case 'Post Production':
        return 'Hậu kỳ';
      default:
        return status;
    }
  }
"""

if "_translateStatus" not in content:
    content = content.replace("  Widget _buildRichText(String label, String value) {", status_translator + "\n  Widget _buildRichText(String label, String value) {")

# Replace Status UI to use _translateStatus
content = content.replace("_buildRichText('${L10n.t('status') ?? 'Trạng thái'}: ', _tmdbDetails!['status'].toString()),", "_buildRichText('${L10n.t('status') ?? 'Trạng thái'}: ', _translateStatus(_tmdbDetails!['status'].toString())),")

# Build the Episodes string if it's a TV show
episode_ui = """
                                            if (_movie!.type == 'series' || _movie!.type == 'hoathinh' || _movie!.type == 'tvshows') ...[
                                              const SizedBox(height: 8),
                                              _buildRichText(
                                                '${L10n.t('episodes') ?? 'Số tập'}: ',
                                                _movie!.totalEpisodes.isNotEmpty && _movie!.totalEpisodes != '?'
                                                    ? '${_movie!.episodes.isNotEmpty ? _movie!.episodes.first.items.length : 0}/${_movie!.totalEpisodes}'
                                                    : '${_movie!.episodes.isNotEmpty ? _movie!.episodes.first.items.length : 0}',
                                              ),
                                            ],
"""

target = """                                          if (_tmdbDetails != null) ...[
                                            if (_tmdbDetails!['status'] != null)
                                              _buildRichText('${L10n.t('status') ?? 'Trạng thái'}: ', _translateStatus(_tmdbDetails!['status'].toString())),"""

if target in content:
    content = content.replace(target, episode_ui + target)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated movie details UI")

import re

with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# 1. Add _getAgeRatingExplanation method
explanation_code = """  String? _getAgeRatingExplanation(String rating) {
    final r = rating.toUpperCase().trim();
    
    // VN
    if (r == 'P') return L10n.t('rating_p') ?? 'Phim phổ biến đến mọi độ tuổi.';
    if (r == 'K') return L10n.t('rating_k') ?? 'Trẻ dưới 13 tuổi cần xem cùng người giám hộ.';
    if (r == 'C13' || r == 'T13') return L10n.t('rating_t13') ?? 'Chỉ dành cho khán giả từ đủ 13 tuổi trở lên.';
    if (r == 'C16' || r == 'T16') return L10n.t('rating_t16') ?? 'Chỉ dành cho khán giả từ đủ 16 tuổi trở lên.';
    if (r == 'C18' || r == 'T18') return L10n.t('rating_t18') ?? 'Chỉ dành cho khán giả từ đủ 18 tuổi trở lên (Chứa nội dung nhạy cảm/bạo lực).';
    if (r == 'C') return 'Phim cấm phổ biến.';

    // US Movies
    if (r == 'G') return L10n.t('rating_g') ?? 'Mọi lứa tuổi (Không chứa yếu tố nhạy cảm).';
    if (r == 'PG') return L10n.t('rating_pg') ?? 'Trẻ em cần sự hướng dẫn của cha mẹ.';
    if (r == 'PG-13') return L10n.t('rating_pg13') ?? 'Cảnh báo trẻ dưới 13 tuổi (Có bạo lực hoặc yếu tố nhạy cảm nhẹ).';
    if (r == 'R') return L10n.t('rating_r') ?? 'Dành cho người trưởng thành. Trẻ dưới 17 tuổi cần cha mẹ đi cùng.';
    if (r == 'NC-17') return L10n.t('rating_nc17') ?? 'Nghiêm cấm trẻ em dưới 17 tuổi.';

    // US TV
    if (r == 'TV-Y') return L10n.t('rating_tv_y') ?? 'Mọi trẻ em.';
    if (r == 'TV-Y7') return L10n.t('rating_tv_y7') ?? 'Trẻ em từ 7 tuổi trở lên.';
    if (r == 'TV-G') return L10n.t('rating_tv_g') ?? 'Mọi lứa tuổi.';
    if (r == 'TV-PG') return L10n.t('rating_tv_pg') ?? 'Cần sự hướng dẫn của phụ huynh.';
    if (r == 'TV-14') return L10n.t('rating_tv_14') ?? 'Dành cho người từ 14 tuổi trở lên.';
    if (r == 'TV-MA') return L10n.t('rating_tv_ma') ?? 'Chỉ dành cho khán giả trưởng thành (Chứa bạo lực mạnh, tình dục hoặc ngôn từ thô tục).';

    // Generic Numbers like 12, 15, 18, 18+
    final match = RegExp(r'^(\d+)\+?$').firstMatch(r);
    if (match != null) {
      return (L10n.t('rating_age_plus') ?? 'Dành cho khán giả từ {age} tuổi trở lên.').replaceAll('{age}', match.group(1)!);
    }
    
    // Default
    return (L10n.t('rating_default') ?? 'Ký hiệu độ tuổi: {rating}').replaceAll('{rating}', rating);
  }

  String? _getAgeRating() {"""

c = c.replace("  String? _getAgeRating() {", explanation_code)

# 2. Update the rendering of Age Rating Badge
old_badge = """                                                if (_getAgeRating() != null)
                                                  _buildBadge(
                                                    _getAgeRating()!,
                                                    ['R', 'NC-17', 'TV-MA', '18+', 'T18', 'C18'].contains(_getAgeRating()) ? Colors.redAccent : Colors.orangeAccent,
                                                  ),"""

# We'll use Tooltip wrapped around _buildBadge
new_badge = """                                                if (_getAgeRating() != null)
                                                  Tooltip(
                                                    message: _getAgeRatingExplanation(_getAgeRating()!) ?? '',
                                                    textStyle: const TextStyle(color: Colors.white, fontSize: 13, height: 1.4),
                                                    decoration: BoxDecoration(
                                                      color: Colors.black.withValues(alpha: 0.85),
                                                      borderRadius: BorderRadius.circular(8),
                                                      border: Border.all(color: Colors.white24),
                                                    ),
                                                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                                                    margin: const EdgeInsets.symmetric(horizontal: 16),
                                                    triggerMode: TooltipTriggerMode.tap,
                                                    child: _buildBadge(
                                                      _getAgeRating()!,
                                                      ['R', 'NC-17', 'TV-MA', '18+', 'T18', 'C18'].contains(_getAgeRating()) ? Colors.redAccent : Colors.orangeAccent,
                                                    ),
                                                  ),"""

# For testing, since the old_badge in dart file might not have T18/C18 check, let's just do a regex replace or precise find
start_idx = c.find("if (_getAgeRating() != null)")
end_idx = c.find("),", c.find("_buildBadge(", start_idx)) + 2

c = c[:start_idx] + new_badge + c[end_idx:]

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Added Tooltip logic to Movie Detail Screen")

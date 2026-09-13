class PremiumParser {
  /// Extracts the season and episode number from any string (filename, slug, name)
  /// Common formats:
  /// - Silo.S01E05.1080p.mkv
  /// - Silo.s01.e05.mkv
  /// - S01E05
  /// - Season 1 Episode 5
  /// - PhA1a 1 TAp 5
  static Map<String, int?> parseSeasonEpisode(String input) {
    if (input.isEmpty) return {'season': null, 'episode': null};

    // Normalize
    final normalized = input.toLowerCase();

    // Pattern 1: S01E05 or S1E5 or s01.e05
    final p1 = RegExp(r's(\d+)\.?e(\d+)');
    final m1 = p1.firstMatch(normalized);
    if (m1 != null) {
      return {
        'season': int.tryParse(m1.group(1)!),
        'episode': int.tryParse(m1.group(2)!),
      };
    }

    // Pattern 2: Season X Episode Y or Ph?n X T?p Y
    final p2 = RegExp(r'(?:season|ph?n|phan|ss|s)\s*(\d+).*?(?:episode|ep|t?p|tap|e)\s*(\d+)');
    final m2 = p2.firstMatch(normalized);
    if (m2 != null) {
      return {
        'season': int.tryParse(m2.group(1)!),
        'episode': int.tryParse(m2.group(2)!),
      };
    }
    
    // Pattern 3: Just Episode
    final p3 = RegExp(r'(?:episode|ep|t?p|tap|e)\s*(\d+)');
    final m3 = p3.firstMatch(normalized);
    
    // Pattern 4: Just Season
    final p4 = RegExp(r'(?:season|ph?n|phan|ss)\s*(\d+)');
    final m4 = p4.firstMatch(normalized);

    return {
      'season': m4 != null ? int.tryParse(m4.group(1)!) : null,
      'episode': m3 != null ? int.tryParse(m3.group(1)!) : null,
    };
  }

  /// Extracts the quality (1080p, 4k, hdr) from filename
  static Map<String, String> parseQuality(String filename) {
    final lower = filename.toLowerCase();
    String hdr = '';
    String audio = '';
    
    if (lower.contains('hdr') || lower.contains('dv') || lower.contains('dovi')) hdr = 'HDR';
    if (lower.contains('1080p')) audio = '1080p'; // using audio as generic tag container for now
    if (lower.contains('4k') || lower.contains('2160p')) audio = '4K';
    if (lower.contains('720p')) audio = '720p';
    
    return {'hdr': hdr, 'audio': audio};
  }
}

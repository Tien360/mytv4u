import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# First, in _fetchPremiumMetadata, we need to save the filename to the premiumEps map so we can use it later?
# Wait, _premiumMetadata is a Map, we can just inject 'filename' into the bestMeta map when saving it!
# Let's modify the new_logic to pass 'filename' in premiumEps, and then when fetching API, insert it into bestMeta.

old_logic = """premiumEps.add({
               'id': uri.pathSegments.last,
               'score': score
            });"""
new_logic = """premiumEps.add({
               'id': uri.pathSegments.last,
               'score': score,
               'filename': ep.filename ?? ''
            });"""
content = content.replace(old_logic, new_logic)

old_check = """for (var id in checkIds) {"""
new_check = """for (var ep in premiumEps.where((e) => e['score'] == maxScore).take(3)) {
      var id = ep['id'].toString();"""
content = content.replace(old_check, new_check)

old_save = """if (score > bestScore) {
            bestScore = score;
            bestMeta = data;
          }"""
new_save = """if (score > bestScore) {
            bestScore = score;
            bestMeta = data;
            bestMeta['fallback_filename'] = ep['filename'];
          }"""
content = content.replace(old_save, new_save)

# Now update _getPremiumQualityText
old_text = """String hdr = (_premiumMetadata!['hdr'] ?? '').toString();
    
    String audio = '';"""
new_text = """String hdr = (_premiumMetadata!['hdr'] ?? '').toString();
    
    // Fallback HDR detection from filename if API returns SDR or Unknown
    if (hdr == 'SDR' || hdr == 'Unknown' || hdr.isEmpty) {
      String fn = (_premiumMetadata!['fallback_filename'] ?? '').toString().toUpperCase();
      if (fn.contains('.DV.') || fn.contains('DOLBY VISION') || fn.contains('DOLBY.VISION')) hdr = 'Dolby Vision';
      else if (fn.contains('HDR10+') || fn.contains('HDR10PLUS')) hdr = 'HDR10+';
      else if (fn.contains('HDR10')) hdr = 'HDR10';
      else if (fn.contains('.HDR.') || fn.contains(' HDR ')) hdr = 'HDR';
    }
    
    String audio = '';"""
content = content.replace(old_text, new_text)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated movie_detail_screen to use filename fallback")

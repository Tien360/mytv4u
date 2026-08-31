import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\api\update_api.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = """  static bool _isNewer(String latest, String current) {
    // Tạm thời so sánh chuỗi đơn giản (String compare).
    // Do cấu trúc năm.tháng.ngày nên so sánh chuỗi hoạt động khá tốt
    // VD: "26.08.08.a" > "26.08.07.b"
    return latest.compareTo(current) > 0;
  }"""

new_logic = """  static bool _isNewer(String latest, String current) {
    List<String> latestParts = latest.split('.');
    List<String> currentParts = current.split('.');
    
    int len = latestParts.length < currentParts.length ? latestParts.length : currentParts.length;
    for (int i = 0; i < len; i++) {
      // Parse thành số để so sánh toán học (tránh lỗi '100' < '99' của chuỗi)
      int? numL = int.tryParse(latestParts[i]);
      int? numC = int.tryParse(currentParts[i]);
      
      if (numL != null && numC != null) {
        if (numL > numC) return true;
        if (numL < numC) return false;
      } else {
        // Fallback về so sánh chuỗi nếu là chữ cái (vd: 'public' vs 'beta')
        int cmp = latestParts[i].compareTo(currentParts[i]);
        if (cmp > 0) return true;
        if (cmp < 0) return false;
      }
    }
    return latestParts.length > currentParts.length;
  }"""

content = content.replace(old_logic, new_logic)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done patching update_api.dart")

import re

with open('lib/api/firebase_api.dart', 'r', encoding='utf-8') as f:
    content = f.read()

new_methods = '''
  // --- User Settings Sync ---
  static Future<void> saveUserSettings(Map<String, dynamic> settings) async {
    final uid = await _getUserId();
    final url = Uri.parse('/userSettings/');
    
    // Convert primitive Dart types to Firestore document format
    final Map<String, dynamic> fields = {};
    settings.forEach((key, value) {
      if (value is String) fields[key] = {'stringValue': value};
      else if (value is int) fields[key] = {'integerValue': value.toString()};
      else if (value is double) fields[key] = {'doubleValue': value};
      else if (value is bool) fields[key] = {'booleanValue': value};
      else if (value is List<String>) {
        fields[key] = {'arrayValue': {'values': value.map((e) => {'stringValue': e}).toList()}};
      }
    });

    try {
      await http.patch(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'fields': fields}),
      );
    } catch (e) {
      print('Error saving user settings: \');
    }
  }

  static Future<Map<String, dynamic>?> loadUserSettings() async {
    final uid = await _getUserId();
    final url = Uri.parse('/userSettings/');
    try {
      final res = await http.get(url);
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        if (data['fields'] != null) {
          final Map<String, dynamic> result = {};
          final fields = data['fields'] as Map<String, dynamic>;
          fields.forEach((key, val) {
            if (val['stringValue'] != null) result[key] = val['stringValue'];
            else if (val['integerValue'] != null) result[key] = int.tryParse(val['integerValue']) ?? 0;
            else if (val['doubleValue'] != null) result[key] = val['doubleValue'] is double ? val['doubleValue'] : double.tryParse(val['doubleValue'].toString()) ?? 0.0;
            else if (val['booleanValue'] != null) result[key] = val['booleanValue'];
            else if (val['arrayValue'] != null && val['arrayValue']['values'] != null) {
              final List values = val['arrayValue']['values'];
              result[key] = values.map((e) => e['stringValue'].toString()).toList();
            }
          });
          return result;
        }
      }
    } catch (e) {
      print('Error loading user settings: \');
    }
    return null;
  }
'''

# Find a good place to insert, right after getAppSettings()
content = content.replace('static Future<Map<String, dynamic>> checkAppStatus() async {', new_methods + '\n  static Future<Map<String, dynamic>> checkAppStatus() async {')

with open('lib/api/firebase_api.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print('Patched firebase_api.dart')

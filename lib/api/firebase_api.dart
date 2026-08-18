import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:math';
import '../models/movie.dart';

class FirebaseApi {
  static const String projectId = 'tv4u-ec4ae';
  static const String baseUrl = 'https://firestore.googleapis.com/v1/projects/$projectId/databases/(default)/documents';

  static Future<String> _getUserId() async {
    final prefs = await SharedPreferences.getInstance();
    String? uid = prefs.getString('firebase_uid');
    if (uid == null) {
      final random = Random();
      uid = 'anon_${DateTime.now().millisecondsSinceEpoch}_${random.nextInt(100000)}';
      await prefs.setString('firebase_uid', uid);
    }
    return uid;
  }

  static Future<void> saveContinueWatching(Movie movie, String currentEpisode) async {
    final uid = await _getUserId();
    final docId = '${uid}_${movie.slug}'.replaceAll(RegExp(r'[^a-zA-Z0-9_]'), '_');
    final url = Uri.parse('$baseUrl/continueWatching/$docId');
    try {
      await http.patch(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'fields': {
            'userId': {'stringValue': uid},
            'movieSlug': {'stringValue': movie.slug},
            'movieName': {'stringValue': movie.name},
            'movieThumb': {'stringValue': movie.thumbUrl},
            'currentEpisode': {'stringValue': currentEpisode},
            'source': {'stringValue': movie.source},
            'originalName': {'stringValue': movie.originalName},
            'type': {'stringValue': movie.type},
            'year': {'stringValue': movie.year},
            'imdbId': {'stringValue': movie.imdbId ?? ''},
            'sourceSlugs': {'stringValue': jsonEncode(movie.sourceSlugs)},
            'lastWatchedAt': {'timestampValue': DateTime.now().toUtc().toIso8601String()},
          }
        }),
      );
    } catch (e) {
      print('Error saving history: $e');
    }
  }

  static Future<List<Map<String, dynamic>>> getContinueWatching() async {
    final uid = await _getUserId();
    final url = Uri.parse('$baseUrl:runQuery');
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'structuredQuery': {
            'from': [{'collectionId': 'continueWatching'}],
            'where': {
              'fieldFilter': {
                'field': {'fieldPath': 'userId'},
                'op': 'EQUAL',
                'value': {'stringValue': uid}
              }
            }
          }
        }),
      );
      if (response.statusCode == 200) {
        final List results = jsonDecode(response.body);
        var mapped = results.where((doc) => doc['document'] != null).map<Map<String, dynamic>>((doc) {
          final fields = doc['document']['fields'];
          return {
            'id': doc['document']['name'].split('/').last,
            'slug': fields['movieSlug']?['stringValue'] ?? '',
            'name': fields['movieName']?['stringValue'] ?? '',
            'thumbUrl': fields['movieThumb']?['stringValue'] ?? '',
            'currentEpisode': fields['currentEpisode']?['stringValue'] ?? '',
            'source': fields['source']?['stringValue'] ?? 'nguonc',
            'originalName': fields['originalName']?['stringValue'] ?? '',
            'type': fields['type']?['stringValue'] ?? '',
            'year': fields['year']?['stringValue'] ?? '',
            'imdbId': fields['imdbId']?['stringValue'] ?? '',
            'sourceSlugs': fields['sourceSlugs']?['stringValue'] ?? '{}',
            'lastWatchedAt': fields['lastWatchedAt']?['timestampValue'] ?? '',
          };
        }).toList();
        mapped.sort((a, b) => b['lastWatchedAt'].compareTo(a['lastWatchedAt']));
        
        // Loại bỏ trùng lặp dựa trên tên phim (nếu người dùng xem 1 phim từ 2 nguồn khác nhau)
        final Map<String, Map<String, dynamic>> deduped = {};
        for (var item in mapped) {
          if (!deduped.containsKey(item['name'])) {
            deduped[item['name']] = item;
          }
        }
        mapped = deduped.values.toList();

        if (mapped.length > 15) {
          final toDelete = mapped.sublist(15);
          mapped = mapped.sublist(0, 15);
          // Xóa các bản ghi cũ trên Firebase (chạy ngầm)
          for (var item in toDelete) {
            http.delete(Uri.parse('$baseUrl/continueWatching/${item['id']}'));
          }
        }
        return mapped;
      }
    } catch (e) {
      print('Error getting history: $e');
    }
    return [];
  }

  static Future<Map<String, dynamic>?> getAppSettings() async {
    final url = Uri.parse('$baseUrl/app_settings/info');
    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['fields'] != null) {
          return {
            'developer': data['fields']['developer']?['stringValue'] ?? 'Chưa cập nhật',
            'contact': data['fields']['contact']?['stringValue'] ?? 'Chưa cập nhật',
            'version': data['fields']['version']?['stringValue'] ?? '1.0.0',
            'facebook': data['fields']['facebook']?['stringValue'] ?? '',
          };
        }
      }
    } catch (e) {
      print('Error fetching app settings: $e');
    }
    return null;
  }

  
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
      print('Error saving user settings: ');
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
      print('Error loading user settings: ');
    }
    return null;
  }

  static Future<Map<String, dynamic>> checkAppStatus() async {
    final url = Uri.parse('$baseUrl/app_settings/status');
    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['fields'] != null) {
          return {
            'isKilled': data['fields']['isKilled']?['booleanValue'] ?? false,
            'killMessage': data['fields']['killMessage']?['stringValue'] ?? 'Ứng dụng đã bị ngừng hoạt động.',
          };
        }
      }
    } catch (e) {
      print('Error fetching app status: $e');
    }
    return {'isKilled': false, 'killMessage': ''};
  }

  static Future<Map<String, dynamic>> getAverageRating(String movieSlug) async {
    final url = Uri.parse('$baseUrl:runQuery');
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'structuredQuery': {
            'from': [{'collectionId': 'ratings'}],
            'where': {
              'fieldFilter': {
                'field': {'fieldPath': 'movieSlug'},
                'op': 'EQUAL',
                'value': {'stringValue': movieSlug}
              }
            }
          }
        }),
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        double totalScore = 0;
        int count = 0;

        for (var item in data) {
          if (item['document'] != null && item['document']['fields'] != null) {
            final fields = item['document']['fields'];
            if (fields['score'] != null) {
              final scoreObj = fields['score'];
              double score = 0;
              if (scoreObj['doubleValue'] != null) {
                score = (scoreObj['doubleValue'] is int) 
                    ? (scoreObj['doubleValue'] as int).toDouble() 
                    : scoreObj['doubleValue'] as double;
              } else if (scoreObj['integerValue'] != null) {
                score = double.parse(scoreObj['integerValue'].toString());
              }
              totalScore += score;
              count++;
            }
          }
        }

        if (count > 0) {
          return {'average': totalScore / count, 'count': count};
        }
      }
    } catch (e) {
      print('Error getting ratings: $e');
    }
    return {'average': 0.0, 'count': 0};
  }

  static Future<int> getUserRating(String movieSlug) async {
    final uid = await _getUserId();
    final url = Uri.parse('$baseUrl/ratings/${uid}_$movieSlug');
    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['fields'] != null && data['fields']['score'] != null) {
          final scoreObj = data['fields']['score'];
          if (scoreObj['integerValue'] != null) {
            return int.parse(scoreObj['integerValue'].toString());
          } else if (scoreObj['doubleValue'] != null) {
            return (scoreObj['doubleValue'] is int) 
                ? scoreObj['doubleValue'] as int 
                : (scoreObj['doubleValue'] as double).toInt();
          }
        }
      }
    } catch (e) {
      print('Error getting user rating: $e');
    }
    return 0;
  }

  static Future<bool> submitRating(String movieSlug, int score) async {
    final uid = await _getUserId();
    final url = Uri.parse(
        '$baseUrl/ratings/${uid}_$movieSlug?updateMask.fieldPaths=score&updateMask.fieldPaths=movieSlug&updateMask.fieldPaths=userId');
    
    try {
      final response = await http.patch(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'fields': {
            'score': {'integerValue': score},
            'movieSlug': {'stringValue': movieSlug},
            'userId': {'stringValue': uid}
          }
        }),
      );
      return response.statusCode == 200;
    } catch (e) {
      print('Error submitting rating: $e');
      return false;
    }
  }

  // --- WATCHLIST ---
  static Future<List<Map<String, dynamic>>> getWatchlist() async {
    final uid = await _getUserId();
    final url = Uri.parse('$baseUrl:runQuery');
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'structuredQuery': {
            'from': [{'collectionId': 'watchlist'}],
            'where': {
              'fieldFilter': {
                'field': {'fieldPath': 'userId'},
                'op': 'EQUAL',
                'value': {'stringValue': uid}
              }
            }
          }
        }),
      );
      if (response.statusCode == 200) {
        final List results = jsonDecode(response.body);
        var mapped = results.where((doc) => doc['document'] != null).map<Map<String, dynamic>>((doc) {
          final fields = doc['document']['fields'];
          return {
            'id': doc['document']['name'].split('/').last,
            'slug': fields['movieSlug']?['stringValue'] ?? '',
            'name': fields['movieName']?['stringValue'] ?? '',
            'thumbUrl': fields['movieThumb']?['stringValue'] ?? '',
            'source': fields['source']?['stringValue'] ?? 'nguonc',
            'addedAt': fields['addedAt']?['timestampValue'] ?? '',
          };
        }).toList();
        mapped.sort((a, b) => b['addedAt'].compareTo(a['addedAt']));
        return mapped;
      }
    } catch (e) {
      print('Error getting watchlist: $e');
    }
    return [];
  }

  static Future<bool> isInWatchlist(String movieSlug) async {
    final uid = await _getUserId();
    final docId = '${uid}_$movieSlug'.replaceAll(RegExp(r'[^a-zA-Z0-9_]'), '_');
    final url = Uri.parse('$baseUrl/watchlist/$docId');
    try {
      final response = await http.get(url);
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }

  static Future<bool> addToWatchlist(Movie movie) async {
    final list = await getWatchlist();
    if (list.length >= 20) {
      return false; // Báo hiệu danh sách đầy
    }

    final uid = await _getUserId();
    final docId = '${uid}_${movie.slug}'.replaceAll(RegExp(r'[^a-zA-Z0-9_]'), '_');
    final url = Uri.parse('$baseUrl/watchlist/$docId');
    try {
      final response = await http.patch(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'fields': {
            'userId': {'stringValue': uid},
            'movieSlug': {'stringValue': movie.slug},
            'movieName': {'stringValue': movie.name},
            'movieThumb': {'stringValue': movie.thumbUrl},
            'source': {'stringValue': movie.source},
            'addedAt': {'timestampValue': DateTime.now().toUtc().toIso8601String()},
          }
        }),
      );
      return response.statusCode == 200;
    } catch (e) {
      print('Error adding to watchlist: $e');
      return false;
    }
  }

  static Future<void> removeFromWatchlist(String movieSlug) async {
    final uid = await _getUserId();
    final docId = '${uid}_$movieSlug'.replaceAll(RegExp(r'[^a-zA-Z0-9_]'), '_');
    final url = Uri.parse('$baseUrl/watchlist/$docId');
    try {
      await http.delete(url);
    } catch (e) {
      print('Error removing from watchlist: $e');
    }
  }
}

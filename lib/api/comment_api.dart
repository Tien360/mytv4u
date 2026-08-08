import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/comment.dart';

class CommentApi {
  static const String _projectId = 'tv4u-ec4ae';
  static const String _database = '(default)';
  static const String _collection = 'comments';
  static const String _baseUrl = 'https://firestore.googleapis.com/v1/projects/$_projectId/databases/$_database/documents';

  static Future<List<Comment>> fetchComments(String movieSlug) async {
    try {
      final url = Uri.parse('$_baseUrl:runQuery');
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'structuredQuery': {
            'from': [{'collectionId': _collection}],
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
        final List<dynamic> data = jsonDecode(utf8.decode(response.bodyBytes));
        List<Comment> comments = [];
        for (var item in data) {
          if (item['document'] != null) {
            final doc = item['document'];
            final name = doc['name'] as String;
            final id = name.split('/').last;
            comments.add(Comment.fromFirestore(id, doc['fields']));
          }
        }
        // Sort newest first by default
        comments.sort((a, b) => b.timestamp.compareTo(a.timestamp));
        return comments;
      }
    } catch (e) {
      print('Error fetching comments: $e');
    }
    return [];
  }

  static Future<Comment?> postComment({
    required String movieSlug,
    required String userId,
    required String userDisplayName,
    required String userPhoto,
    required String text,
  }) async {
    try {
      final url = Uri.parse('$_baseUrl/$_collection');
      final timestamp = DateTime.now().toUtc();
      final body = jsonEncode({
        'fields': {
          'movieSlug': {'stringValue': movieSlug},
          'userId': {'stringValue': userId},
          'userDisplayName': {'stringValue': userDisplayName},
          'userPhoto': {'stringValue': userPhoto},
          'text': {'stringValue': text.trim()},
          'timestamp': {'timestampValue': timestamp.toIso8601String()},
          'replies': {'arrayValue': {'values': []}}
        }
      });

      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: body,
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        final doc = jsonDecode(utf8.decode(response.bodyBytes));
        final name = doc['name'] as String;
        final id = name.split('/').last;
        return Comment.fromFirestore(id, doc['fields']);
      } else {
        print('Error posting comment: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      print('Exception posting comment: $e');
    }
    return null;
  }
  static Future<CommentReply?> replyToComment({
    required String parentId,
    required String userId,
    required String userDisplayName,
    required String userPhoto,
    required String text,
  }) async {
    try {
      final url = Uri.parse('https://firestore.googleapis.com/v1/projects/$_projectId/databases/$_database/documents:commit');
      final replyId = DateTime.now().millisecondsSinceEpoch.toString();
      final timestamp = DateTime.now().toUtc().toIso8601String();

      final replyObj = {
        'mapValue': {
          'fields': {
            'id': {'stringValue': replyId},
            'userId': {'stringValue': userId},
            'userDisplayName': {'stringValue': userDisplayName},
            'userPhoto': {'stringValue': userPhoto},
            'text': {'stringValue': text.trim()},
            'timestamp': {'timestampValue': timestamp}
          }
        }
      };

      final body = jsonEncode({
        'writes': [
          {
            'transform': {
              'document': 'projects/$_projectId/databases/$_database/documents/$_collection/$parentId',
              'fieldTransforms': [
                {
                  'fieldPath': 'replies',
                  'appendMissingElements': {
                    'values': [replyObj]
                  }
                }
              ]
            }
          }
        ]
      });

      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: body,
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        return CommentReply(
          id: replyId,
          userId: userId,
          userDisplayName: userDisplayName,
          userPhoto: userPhoto,
          text: text.trim(),
          timestamp: DateTime.parse(timestamp),
        );
      } else {
        print('Error posting reply: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      print('Exception posting reply: $e');
    }
    return null;
  }
}

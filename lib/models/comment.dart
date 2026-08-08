class Comment {
  final String id;
  final String movieSlug;
  final String userId;
  final String userDisplayName;
  final String userPhoto;
  final String text;
  final DateTime timestamp;
  final List<CommentReply> replies;

  Comment({
    required this.id,
    required this.movieSlug,
    required this.userId,
    required this.userDisplayName,
    required this.userPhoto,
    required this.text,
    required this.timestamp,
    required this.replies,
  });

  factory Comment.fromFirestore(String id, Map<String, dynamic> doc) {
    List<CommentReply> parsedReplies = [];
    if (doc['replies'] != null && doc['replies']['arrayValue'] != null && doc['replies']['arrayValue']['values'] != null) {
      final list = doc['replies']['arrayValue']['values'] as List;
      parsedReplies = list.map((e) => CommentReply.fromMap(e['mapValue']['fields'])).toList();
    }

    return Comment(
      id: id,
      movieSlug: doc['movieSlug']?['stringValue'] ?? '',
      userId: doc['userId']?['stringValue'] ?? '',
      userDisplayName: doc['userDisplayName']?['stringValue'] ?? 'Khách',
      userPhoto: doc['userPhoto']?['stringValue'] ?? 'https://via.placeholder.com/150',
      text: doc['text']?['stringValue'] ?? '',
      timestamp: doc['timestamp']?['timestampValue'] != null
          ? DateTime.parse(doc['timestamp']['timestampValue'])
          : DateTime.now(),
      replies: parsedReplies,
    );
  }
}

class CommentReply {
  final String id;
  final String userId;
  final String text;
  final String userDisplayName;
  final String userPhoto;
  final DateTime timestamp;

  CommentReply({
    required this.id,
    required this.userId,
    required this.text,
    required this.userDisplayName,
    required this.userPhoto,
    required this.timestamp,
  });

  factory CommentReply.fromMap(Map<String, dynamic> map) {
    DateTime parsedTime = DateTime.now();
    if (map['timestamp'] != null) {
      if (map['timestamp']['stringValue'] != null) {
        parsedTime = DateTime.parse(map['timestamp']['stringValue']);
      } else if (map['timestamp']['timestampValue'] != null) {
        parsedTime = DateTime.parse(map['timestamp']['timestampValue']);
      }
    }
    
    return CommentReply(
      id: map['id']?['stringValue'] ?? '',
      userId: map['userId']?['stringValue'] ?? '',
      text: map['text']?['stringValue'] ?? '',
      userDisplayName: map['userDisplayName']?['stringValue'] ?? 'Khách',
      userPhoto: map['userPhoto']?['stringValue'] ?? 'https://via.placeholder.com/150',
      timestamp: parsedTime,
    );
  }
}

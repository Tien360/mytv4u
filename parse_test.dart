import 'dart:convert';
import 'dart:io';

void main() {
  final jsonString = File('out_free1.json').readAsStringSync();
  final data = json.decode(jsonString);
  final epsList = data['episodes'] as List?;
  if (epsList == null) {
      print('epsList is null');
      return;
  }
  
  for (var srv in epsList) {
        String rawName = srv['server_name'] ?? 'Server';
        final serverName = 'Free1 - $rawName';
  
        List epItems = [];
        if (srv['server_data'] is List) {
          epItems = srv['server_data'];
        } else if (srv['items'] is List) {
          epItems = srv['items'];
        }
        
        print('Server: $serverName, epItems count: ${epItems.length}');
        
        for (var ep in epItems) {
           print('  ep name: ${ep['name']}');
        }
  }
}

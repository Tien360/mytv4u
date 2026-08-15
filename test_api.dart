import 'dart:convert'; 
import 'package:http/http.dart' as http; 
void main() async { 
  var res = await http.get(Uri.parse('https://ophim1.com/v1/api/danh-sach/phim-le?page=1')); 
  print('Ophim: ' + res.statusCode.toString()); 
  res = await http.get(Uri.parse('https://phimapi.com/v1/api/danh-sach/phim-bo?page=1')); 
  print('PhimAPI: ' + res.statusCode.toString()); 
}

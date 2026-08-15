import 'dart:convert'; 
import 'package:http/http.dart' as http; 
void main() async { 
  var res = await http.get(Uri.parse('https://ophim1.com/v1/api/danh-sach/phim-le?page=1')); 
  var data = jsonDecode(res.body); 
  print(data['data']['items'].length); 
}

import 'package:http/http.dart' as http;
import 'package:html/parser.dart' as html_parser;

class TvChannel {
  final String id;
  final String name;
  final String category;
  final String logo;
  final String streamUrl;
  final String webUrl;
  final String description;

  TvChannel({
    required this.id,
    required this.name,
    required this.category,
    required this.logo,
    required this.streamUrl,
    this.webUrl = '',
    this.description = '',
  });

  TvChannel copyWith({
    String? id,
    String? name,
    String? category,
    String? logo,
    String? streamUrl,
    String? webUrl,
    String? description,
  }) {
    return TvChannel(
      id: id ?? this.id,
      name: name ?? this.name,
      category: category ?? this.category,
      logo: logo ?? this.logo,
      streamUrl: streamUrl ?? this.streamUrl,
      webUrl: webUrl ?? this.webUrl,
      description: description ?? this.description,
    );
  }

  factory TvChannel.fromJson(Map<String, dynamic> json) {
    return TvChannel(
      id: json['id'] ?? json['name'] ?? '',
      name: json['name'] ?? '',
      category: json['category'] ?? 'TV',
      logo: json['logo'] ?? '',
      streamUrl: json['streamUrl'] ?? json['url'] ?? '',
      webUrl: json['webUrl'] ?? '',
      description: json['description'] ?? '',
    );
  }
}

class TvApi {
  static final List<TvChannel> defaultChannels = [
    // ------------------- VTV (Quốc Gia) -------------------
    TvChannel(
      id: 'vtv1',
      name: 'VTV1 HD',
      category: 'VTV',
      logo: '',
      streamUrl: 'https://live-a.fptplay53.net/live/media/vtv1/live247-hls-avc/index.m3u8',
      webUrl: 'https://tv360.vn/tv/vtv1-hd?ch=2&c=0',
      description: 'Kênh Thời sự - Chính trị - Tổng hợp Đài Truyền hình Việt Nam',
    ),
    TvChannel(
      id: 'vtv2',
      name: 'VTV2 HD',
      category: 'VTV',
      logo: '',
      streamUrl: 'https://live-a.fptplay53.net/live/media/vtv2/live247-hls-avc/index.m3u8',
      webUrl: 'https://tv360.vn/tv/vtv2-hd?ch=3&c=0',
      description: 'Kênh Khoa học - Giáo dục',
    ),
    TvChannel(
      id: 'vtv3',
      name: 'VTV3 HD',
      category: 'VTV',
      logo: '',
      streamUrl: 'https://live-a.fptplay53.net/live/media/vtv3/live247-hls-avc/index.m3u8',
      webUrl: 'https://tv360.vn/tv/vtv3-hd?ch=4&c=0',
      description: 'Kênh Thể thao - Văn hóa - Giải trí Thông tin',
    ),
    TvChannel(
      id: 'vtv4',
      name: 'VTV4 HD',
      category: 'VTV',
      logo: '',
      streamUrl: 'https://live-a.fptplay53.net/live/media/vtv4/live247-hls-avc/index.m3u8',
      webUrl: 'https://tv360.vn/tv/vtv4-hd?ch=5&c=0',
      description: 'Kênh Đối ngoại Đài Truyền hình Việt Nam',
    ),
    TvChannel(
      id: 'vtv5',
      name: 'VTV5 HD',
      category: 'VTV',
      logo: '',
      streamUrl: 'https://live-a.fptplay53.net/live/media/vtv5/live247-hls-avc/index.m3u8',
      webUrl: 'https://tv360.vn/tv/vtv5-hd?ch=110&c=0',
      description: 'Kênh Truyền hình tiếng Dân tộc',
    ),
    TvChannel(
      id: 'vtv5tnb',
      name: 'VTV5 Tây Nam Bộ',
      category: 'VTV',
      logo: '',
      streamUrl: 'https://live-a.fptplay53.net/live/media/vtv5tnb/live-hls-avc/index.m3u8',
      description: 'Kênh Truyền hình khu vực Tây Nam Bộ',
    ),
    TvChannel(
      id: 'vtv5tn',
      name: 'VTV5 Tây Nguyên',
      category: 'VTV',
      logo: '',
      streamUrl: 'https://live-a.fptplay53.net/live/media/vtv5tn/live-hls-avc/index.m3u8',
      description: 'Kênh Truyền hình khu vực Tây Nguyên',
    ),
    TvChannel(
      id: 'vtv7',
      name: 'VTV7 HD',
      category: 'VTV',
      logo: '',
      streamUrl: 'https://live-a.fptplay53.net/live/media/vtv7/live247-hls-avc/index.m3u8',
      webUrl: 'https://tv360.vn/tv/vtv7-hd?ch=138&c=0',
      description: 'Kênh Truyền hình Giáo dục Quốc gia',
    ),
    TvChannel(
      id: 'vtv8',
      name: 'VTV8 HD',
      category: 'VTV',
      logo: '',
      streamUrl: 'https://live-a.fptplay53.net/live/media/vtv8/live-hls-avc/index.m3u8',
      webUrl: 'https://tv360.vn/tv/vtv8-hd?ch=139&c=0',
      description: 'Kênh Truyền hình Miền Trung - Tây Nguyên',
    ),
    TvChannel(
      id: 'vtv9',
      name: 'VTV9 HD',
      category: 'VTV',
      logo: '',
      streamUrl: 'https://live-a.fptplay53.net/live/media/vtv9/live247-hls-avc/index.m3u8',
      webUrl: 'https://tv360.vn/tv/vtv9-hd?ch=140&c=0',
      description: 'Kênh Truyền hình khu vực Nam Bộ',
    ),
    TvChannel(
      id: 'vtv10',
      name: 'VTV Cần Thơ',
      category: 'VTV',
      logo: '',
      streamUrl: 'https://live-a.fptplay53.net/live/media/vtv10/live247-hls-avc/index.m3u8',
      description: 'Kênh Truyền hình Quốc gia VTV Cần Thơ',
    ),

    // ------------------- VTVcab & HTV & VTC -------------------
    TvChannel(
      id: 'vtvcab1',
      name: 'VTVcab 1 - ON Vie Giải Trí',
      category: 'HTV & VTC',
      logo: '',
      streamUrl: '',
      webUrl: 'https://tv360.vn/tv/vtvcab1-vie-giai-tri-hd?ch=201&c=0',
      description: 'Kênh Phim & Giải trí Hàng đầu VTVcab (Xem qua WebView TV360)',
    ),
    TvChannel(
      id: 'vtvcab2',
      name: 'VTVcab 2 - ON Phim Việt',
      category: 'HTV & VTC',
      logo: '',
      streamUrl: '',
      webUrl: 'https://tv360.vn/tv/vtvcab2-phim-viet-hd?ch=202&c=0',
      description: 'Kênh Phim Việt Nam Đặc Sắc VTVcab (Xem qua WebView TV360)',
    ),
    TvChannel(
      id: 'vtvcab10',
      name: 'VTVcab 10 - ON Cine HD',
      category: 'HTV & VTC',
      logo: '',
      streamUrl: '',
      webUrl: 'https://tv360.vn/tv/vtvcab10-on-cine-hd?ch=210&c=0',
      description: 'Kênh Điện ảnh Quốc tế VTVcab (Xem qua WebView TV360)',
    ),
    TvChannel(
      id: 'vtvcab19',
      name: 'VTVcab 19 - ON Vie Dramas',
      category: 'HTV & VTC',
      logo: '',
      streamUrl: '',
      webUrl: 'https://tv360.vn/tv/vtvcab19-vie-dramas?ch=219&c=0',
      description: 'Kênh Phim Truyền hình Châu Á VTVcab (Xem qua WebView TV360)',
    ),
    TvChannel(
      id: 'vtvcab8',
      name: 'VTVcab 8 - ON BiBi',
      category: 'HTV & VTC',
      logo: '',
      streamUrl: '',
      webUrl: 'https://tv360.vn/tv/vtvcab8-bibi-sd?ch=208&c=0',
      description: 'Kênh Thiếu Nhi BiBi VTVcab (Xem qua WebView TV360)',
    ),
    TvChannel(
      id: 'vtvcab4',
      name: 'VTVcab 4 - ON Movies HD',
      category: 'HTV & VTC',
      logo: '',
      streamUrl: '',
      webUrl: 'https://tv360.vn/tv/vtvcab4-on-movies?ch=204&c=0',
      description: 'Kênh Phim Điện Ảnh bom tấn (Xem qua WebView TV360)',
    ),
    TvChannel(
      id: 'vtvcab5',
      name: 'VTVcab 5 - ON E Channel',
      category: 'HTV & VTC',
      logo: '',
      streamUrl: '',
      webUrl: 'https://tv360.vn/tv/vtvcab5-e-channel-hd?ch=205&c=0',
      description: 'Kênh Giải trí Phong cách sống (Xem qua WebView TV360)',
    ),
    TvChannel(
      id: 'vtvcab15',
      name: 'VTVcab 15 - ON Music HD',
      category: 'HTV & VTC',
      logo: '',
      streamUrl: '',
      webUrl: 'https://tv360.vn/tv/vtvcab15-on-music?ch=215&c=0',
      description: 'Kênh Âm nhạc Giải trí (Xem qua WebView TV360)',
    ),
    TvChannel(
      id: 'htv1',
      name: 'HTV1 HD',
      category: 'HTV & VTC',
      logo: '',
      streamUrl: 'https://live.fptplay53.net/epzhd1/htv1_vhls.smil/chunklist.m3u8',
      description: 'Kênh Thông tin Công cộng Đài HTV',
    ),
    TvChannel(
      id: 'htv3',
      name: 'HTV3 HD',
      category: 'HTV & VTC',
      logo: '',
      streamUrl: 'https://live.fptplay53.net/epzhd1/htv3_vhls.smil/chunklist.m3u8',
      description: 'Kênh Thanh Thiếu nhi & Gia đình Đài HTV',
    ),
    TvChannel(
      id: 'htv4',
      name: 'HTV4 HD',
      category: 'HTV & VTC',
      logo: '',
      streamUrl: 'https://live.fptplay53.net/epzhd1/htv4_vhls.smil/chunklist.m3u8',
      description: 'Kênh Dạy học & Tri thức Đài HTV',
    ),
    TvChannel(
      id: 'htv7',
      name: 'HTV7 HD',
      category: 'HTV & VTC',
      logo: '',
      streamUrl: 'https://live-a.fptplay53.net/live/media/htv7/live247-hls-avc/index.m3u8',
      webUrl: 'https://tv360.vn/tv/htv7-hd?ch=193&c=0',
      description: 'Kênh Văn hóa - Giải trí Đài HTV',
    ),
    TvChannel(
      id: 'htv9',
      name: 'HTV9 HD',
      category: 'HTV & VTC',
      logo: '',
      streamUrl: 'https://live-a.fptplay53.net/live/media/htv9/live247-hls-avc/index.m3u8',
      webUrl: 'https://tv360.vn/tv/htv9-hd?ch=194&c=0',
      description: 'Kênh Thông tin - Thời sự Đài HTV',
    ),
    TvChannel(
      id: 'htvkey',
      name: 'HTV Key HD',
      category: 'HTV & VTC',
      logo: '',
      streamUrl: 'https://liveh12.vtvprime.vn/hls/HTVKey/index.m3u8',
      description: 'Kênh Giáo dục & Khoa học Đài HTV',
    ),
    TvChannel(
      id: 'htvtt',
      name: 'HTV Thể thao HD',
      category: 'HTV & VTC',
      logo: '',
      streamUrl: 'https://live.fptplay53.net/epzhd1/htvcthethao_vhls.smil/chunklist.m3u8',
      description: 'Kênh Thể thao Chuyên biệt Đài HTV',
    ),
    TvChannel(
      id: 'antv',
      name: 'ANTV HD',
      category: 'HTV & VTC',
      logo: '',
      streamUrl: 'https://liveh12.vtvprime.vn/hls/ANNINHTV/index.m3u8',
      webUrl: 'https://tv360.vn/tv/antv?ch=20&c=0',
      description: 'Kênh Truyền hình Công an Nhân dân',
    ),
    TvChannel(
      id: 'qpvn',
      name: 'QPVN HD',
      category: 'HTV & VTC',
      logo: '',
      streamUrl: 'https://liveh12.vtvprime.vn/hls/QPTV/index.m3u8',
      webUrl: 'https://tv360.vn/tv/qpvn-hd?ch=19&c=0',
      description: 'Kênh Truyền hình Quốc phòng Việt Nam',
    ),
    TvChannel(
      id: 'sctv2',
      name: 'SCTV2 HD',
      category: 'HTV & VTC',
      logo: '',
      streamUrl: 'https://liveh12.vtvprime.vn/hls/SCTV2/index.m3u8',
      description: 'Kênh Phim truyện SCTV',
    ),
    TvChannel(
      id: 'sctv6',
      name: 'SCTV6 HD',
      category: 'HTV & VTC',
      logo: '',
      streamUrl: 'https://live.fptplay53.net/epzhd2/film360_vhls.smil/chunklist.m3u8',
      description: 'Kênh Phim tổng hợp SCTV6',
    ),

    // ------------------- Truyền Hình Tỉnh -------------------
    TvChannel(
      id: 'thvl1',
      name: 'THVL1 HD (Vĩnh Long 1)',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'https://live-a.fptplay53.net/live/media/vinhlong1/live247-hls-avc/index.m3u8',
      webUrl: 'https://tv360.vn/tv/vinh-long-1?ch=76&c=0',
      description: 'Kênh Tổng hợp Truyền hình Vĩnh Long 1',
    ),
    TvChannel(
      id: 'thvl2',
      name: 'THVL2 HD (Vĩnh Long 2)',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'https://live-a.fptplay53.net/live/media/vinhlong2/live247-hls-avc/index.m3u8',
      webUrl: 'https://tv360.vn/tv/vinh-long-2?ch=77&c=0',
      description: 'Kênh Phim & Giải trí Truyền hình Vĩnh Long 2',
    ),
    TvChannel(
      id: 'thvl3',
      name: 'THVL3 HD (Vĩnh Long 3)',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'https://live-a.fptplay53.net/live/media/vinhlong3/live247-hls-avc/index.m3u8',
      webUrl: 'https://tv360.vn/tv/vinh-long-3?ch=78&c=0',
      description: 'Kênh Văn hóa - Nông nghiệp Truyền hình Vĩnh Long 3',
    ),
    TvChannel(
      id: 'hanoi1',
      name: 'Hà Nội 1 (HN1)',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'https://liveh34.vtvprime.vn/hls/HANOI1TV/index.m3u8',
      webUrl: 'https://tv360.vn/tv/ha-noi-1?ch=60&c=0',
      description: 'Kênh Thời sự - Chính trị Đài Hà Nội',
    ),
    TvChannel(
      id: 'hanoi2',
      name: 'Hà Nội 2 (HN2)',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'https://cloudstreamhntv.tek4tv.vn/live/smil:HN2.smil/playlist.m3u8',
      webUrl: 'https://tv360.vn/tv/ha-noi-2?ch=61&c=0',
      description: 'Kênh Văn hóa - Xã hội Đài Hà Nội',
    ),
    TvChannel(
      id: 'haiphong',
      name: 'Hải Phòng TV (THP)',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'https://live-a.fptplay53.net/live/media/haiphong/live-hls-avc/index.m3u8',
      webUrl: 'https://tv360.vn/tv/hai-phong?ch=55&c=0',
      description: 'Kênh Truyền hình Thành phố Hải Phòng',
    ),
    TvChannel(
      id: 'danang1',
      name: 'Đà Nẵng TV1 HD',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'https://live.mediatech.vn/live/285b59a111d76974225a8e3004bfc31a509/chunklist.m3u8',
      webUrl: 'https://tv360.vn/tv/da-nang-1?ch=67&c=0',
      description: 'Kênh Truyền hình Thành phố Đà Nẵng 1',
    ),
    TvChannel(
      id: 'nghean',
      name: 'Nghệ An TV HD',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'https://live.mediatech.vn/live/2859591eef2e92249b682db021f4247c364/chunklist.m3u8',
      webUrl: 'https://tv360.vn/tv/nghe-an?ch=53&c=0',
      description: 'Kênh Truyền hình Nghệ An',
    ),
    TvChannel(
      id: 'quangngai',
      name: 'Quảng Ngãi TV',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'https://live.mediatech.vn/live/285aaa79b4b265a457d81bb72bc32e2c114/chunklist.m3u8',
      description: 'Kênh Truyền hình Quảng Ngãi',
    ),
    TvChannel(
      id: 'dongthap1',
      name: 'Đồng Tháp 1 HD',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'https://liveh34.vtvprime.vn/hls/DONGTHAPTV/index.m3u8',
      webUrl: 'https://tv360.vn/tv/dong-thap-1?ch=69&c=0',
      description: 'Kênh Thời sự - Tổng hợp Đồng Tháp',
    ),
    TvChannel(
      id: 'cantho1',
      name: 'Cần Thơ 1 HD',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'https://live.canthotv.vn/live/tv/chunklist.m3u8',
      webUrl: 'https://tv360.vn/tv/can-tho-1?ch=63&c=0',
      description: 'Kênh Truyền hình Thành phố Cần Thơ',
    ),
    TvChannel(
      id: 'angiang1',
      name: 'An Giang TV1 HD',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'https://tv.angiangtv.vn/live/kgtv/kgtv.m3u8',
      description: 'Kênh Truyền hình An Giang 1',
    ),
    TvChannel(
      id: 'angiang2',
      name: 'An Giang TV2 HD',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'https://tv.angiangtv.vn/live/kgtv2/kgtv2.m3u8',
      description: 'Kênh Truyền hình An Giang 2',
    ),
    TvChannel(
      id: 'camau',
      name: 'Cà Mau TV',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'https://tv.ctvcamau.vn/live/tv/tv.m3u8',
      description: 'Kênh Truyền hình Cà Mau',
    ),

    TvChannel(
      id: 'caobang',
      name: 'Cao Bằng TV',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'https://stream.thingnet.vn/live/smil:CRTV.smil/chunklist.m3u8',
      description: 'Kênh Truyền hình Cao Bằng',
    ),
    TvChannel(
      id: 'dienbien',
      name: 'Điện Biên TV',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'https://truyenhinh.vnptvas.vn/live.m3u8?c=vstv362&gcId=1532&pkg=pkg11.hni&q=high',
      description: 'Kênh Truyền hình Điện Biên',
    ),
    TvChannel(
      id: 'dongnai1',
      name: 'Đồng Nai 1',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'http://118.107.85.4:1935/live/smil:DNTV1.smil/chunklist.m3u8',
      description: 'Kênh Truyền hình Đồng Nai 1',
    ),
    TvChannel(
      id: 'dongnai2',
      name: 'Đồng Nai 2',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'http://118.107.85.4:1935/live/smil:DNTV2.smil/chunklist.m3u8',
      description: 'Kênh Truyền hình Đồng Nai 2',
    ),
    TvChannel(
      id: 'dongthap2',
      name: 'Đồng Tháp 2',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'https://618b88f69e53b.streamlock.net/THDT2/thdttv2/chunklist.m3u8',
      description: 'Kênh Truyền hình Đồng Tháp 2',
    ),

    TvChannel(
      id: 'hue',
      name: 'Thừa Thiên Huế (TRT)',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'https://live.fptplay53.net/epzsd1/hue_hls.smil/chunklist.m3u8',
      description: 'Kênh Truyền hình Thừa Thiên Huế',
    ),

    TvChannel(
      id: 'lamdong',
      name: 'Lâm Đồng TV (LTV)',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'http://118.107.85.5:1935/live/smil:LTV.smil/chunklist.m3u8',
      description: 'Kênh Truyền hình Lâm Đồng',
    ),
    TvChannel(
      id: 'tayninh',
      name: 'Tây Ninh TV',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'https://live-hq.evgcdn.net/live/2851dc2c9af68834814a89e61db0faee561/chunklist.m3u8',
      description: 'Kênh Truyền hình Tây Ninh',
    ),
    TvChannel(
      id: 'thainguyen',
      name: 'Thái Nguyên TV',
      category: 'Truyền Hình Tỉnh',
      logo: '',
      streamUrl: 'https://streaming.thainguyentv.vn/hls/livestream.m3u8',
      description: 'Kênh Truyền hình Thái Nguyên',
    ),

    // ------------------- Kênh Quốc Tế (Kết hợp Luồng HD Trực tiếp & TV360 Web) -------------------
    TvChannel(
      id: 'outdoor',
      name: 'Outdoor Channel HD',
      category: 'Kênh Quốc Tế',
      logo: '',
      streamUrl: '',
      webUrl: 'https://tv360.vn/tv/outdoor-hd?ch=150&c=0',
      description: 'Kênh Thể Thao Dã Ngoại Quốc Tế (Xem qua WebView TV360)',
    ),
    TvChannel(
      id: 'afn',
      name: 'Asian Food Network (AFN)',
      category: 'Kênh Quốc Tế',
      logo: '',
      streamUrl: '',
      webUrl: 'https://tv360.vn/tv/afn-hd?ch=151&c=0',
      description: 'Kênh Ẩm Thực Châu Á Hàng Đầu (Xem qua WebView TV360)',
    ),
    TvChannel(
      id: 'history',
      name: 'History HD',
      category: 'Kênh Quốc Tế',
      logo: '',
      streamUrl: '',
      webUrl: 'https://tv360.vn/tv/history-hd?ch=152&c=0',
      description: 'Kênh Lịch Sử & Khám Phá Thế Giới (Xem qua WebView TV360)',
    ),
    TvChannel(
      id: 'kix',
      name: 'KIX HD',
      category: 'Kênh Quốc Tế',
      logo: '',
      streamUrl: '',
      webUrl: 'https://tv360.vn/tv/kix?ch=153&c=0',
      description: 'Kênh Phim Hành Động Võ Thuật Châu Á (Xem qua WebView TV360)',
    ),
    TvChannel(
      id: 'hgtv',
      name: 'HGTV HD',
      category: 'Kênh Quốc Tế',
      logo: '',
      streamUrl: '',
      webUrl: 'https://tv360.vn/tv/hgtv?ch=154&c=0',
      description: 'Kênh Nhà Đẹp & Trang Trí Nội Thất (Xem qua WebView TV360)',
    ),
    TvChannel(
      id: 'davinci',
      name: 'Da Vinci HD',
      category: 'Kênh Quốc Tế',
      logo: '',
      streamUrl: '',
      webUrl: 'https://tv360.vn/tv/davinci-hd?ch=155&c=0',
      description: 'Kênh Giáo Dục & Khám Phá Trẻ Em (Xem qua WebView TV360)',
    ),
    TvChannel(
      id: 'cnbc',
      name: 'CNBC International',
      category: 'Kênh Quốc Tế',
      logo: '',
      streamUrl: '',
      webUrl: 'https://tv360.vn/tv/cnbc?ch=156&c=0',
      description: 'Kênh Tin Tức Kinh Tế Tài Chính Mỹ (Xem qua WebView TV360)',
    ),

    TvChannel(
      id: 'tv5monde',
      name: 'TV5Monde Asia HD',
      category: 'Kênh Quốc Tế',
      logo: '',
      streamUrl: 'https://liveh12.vtvprime.vn/hls/TV5/03.m3u8',
      webUrl: 'https://tv360.vn/tv/tv5?ch=158&c=0',
      description: 'Kênh Truyền hình Quốc tế Tiếng Pháp Châu Á (TV5Monde)',
    ),
    TvChannel(
      id: 'euronews',
      name: 'Euronews English HD',
      category: 'Kênh Quốc Tế',
      logo: '',
      streamUrl: 'https://cdn-euronews.akamaized.net/live/eds/euronews-en/25002/index.m3u8',
      description: 'Kênh Tin tức Quốc tế Hàng đầu Châu Âu',
    ),
    TvChannel(
      id: 'dwnews',
      name: 'DW News HD (Đức)',
      category: 'Kênh Quốc Tế',
      logo: '',
      streamUrl: 'https://dwamdstream102.akamaized.net/hls/live/2015525/dwstream102/master.m3u8',
      webUrl: 'https://tv360.vn/tv/dw?ch=159&c=0',
      description: 'Kênh Tin tức Thời sự Quốc tế Deutsche Welle (Đức)',
    ),
    TvChannel(
      id: 'france24en',
      name: 'France 24 English HD',
      category: 'Kênh Quốc Tế',
      logo: '',
      streamUrl: 'https://live.france24.com/hls/live/2037218-b/F24_EN_HI_HLS/master_5000.m3u8',
      webUrl: 'https://tv360.vn/tv/france-24?ch=160&c=0',
      description: 'Kênh Tin tức Quốc tế Tiếng Anh (Pháp)',
    ),
    TvChannel(
      id: 'france24fr',
      name: 'France 24 Français HD',
      category: 'Kênh Quốc Tế',
      logo: '',
      streamUrl: 'https://live.france24.com/hls/live/2037179-b/F24_FR_HI_HLS/master_5000.m3u8',
      webUrl: 'https://tv360.vn/tv/france-24-sd?ch=161&c=0',
      description: 'Kênh Tin tức Quốc tế Tiếng Pháp',
    ),
    TvChannel(
      id: 'nhkworld',
      name: 'NHK World-Japan HD',
      category: 'Kênh Quốc Tế',
      logo: '',
      streamUrl: 'https://masterpl.hls.nhkworld.jp/hls/w/live/smarttv.m3u8',
      webUrl: 'https://tv360.vn/tv/nhk?ch=162&c=0',
      description: 'Kênh Truyền hình Tin tức & Văn hóa Nhật Bản',
    ),
    TvChannel(
      id: 'arirang',
      name: 'Arirang TV HD',
      category: 'Kênh Quốc Tế',
      logo: '',
      streamUrl: 'http://amdlive-ch01.ctnd.com.edgesuite.net/arirang_1ch/smil:arirang_1ch.smil/playlist.m3u8',
      webUrl: 'https://tv360.vn/tv/arirang?ch=163&c=0',
      description: 'Kênh Truyền hình Văn hóa & Giải trí Hàn Quốc',
    ),
    TvChannel(
      id: 'bbcnews',
      name: 'BBC News HD',
      category: 'Kênh Quốc Tế',
      logo: '',
      streamUrl: 'http://46.32.176.50/bbcworld/index.m3u8',
      description: 'Kênh Tin tức Quốc tế Hàng đầu Anh Quốc (BBC)',
    ),
    TvChannel(
      id: 'bloomberg',
      name: 'Bloomberg TV HD',
      category: 'Kênh Quốc Tế',
      logo: '',
      streamUrl: 'https://bloomberg.com/media-manifest/streams/us.m3u8',
      webUrl: 'https://tv360.vn/tv/bloomberg?ch=164&c=0',
      description: 'Kênh Tin tức Tài chính & Kinh tế Quốc tế Mỹ',
    ),
    TvChannel(
      id: 'fashiontv',
      name: 'FashionTV Paris HD',
      category: 'Kênh Quốc Tế',
      logo: '',
      streamUrl: 'https://edge-fast3.evrideo.tv/bfdbb576-83f7-11f0-9f89-0200170e3e04_1000028043_HLS/manifest.m3u8',
      webUrl: 'https://tv360.vn/tv/fashiontv?ch=165&c=0',
      description: 'Kênh Thời trang & Phong cách sống Đỉnh cao Pháp',
    ),
    TvChannel(
      id: 'nasatv',
      name: 'NASA TV HD',
      category: 'Kênh Quốc Tế',
      logo: '',
      streamUrl: 'https://ntv1.akamaized.net/hls/live/2014075/NASA-NTV1-HLS/master.m3u8',
      description: 'Kênh Truyền hình Khoa học & Vũ trụ Cơ quan NASA Mỹ',
    ),
    TvChannel(
      id: 'tvbvietnam',
      name: 'TVB Vietnam HD',
      category: 'Kênh Quốc Tế',
      logo: '',
      streamUrl: 'https://amg01868-amg01868c3-tvbanywhere-us-4491.playouts.now.amagi.tv/playlist/amg01868-tvbusa-tvbvietnam-tvbanywhereus/playlist.m3u8',
      description: 'Kênh Phim TVB Lồng Tiếng Việt',
    ),
    TvChannel(
      id: 'vietnamtoday',
      name: 'Vietnam Today HD',
      category: 'Kênh Quốc Tế',
      logo: '',
      streamUrl: 'https://vips-livecdn.fptplay.net/live/media/vietnamtoday/live-hls-avc/index.m3u8',
      description: 'Kênh Tin tức & Văn hóa Việt Nam Quốc tế',
    ),
  ];

  static Future<List<TvChannel>> getChannels() async {
    List<TvChannel> channels = List.from(defaultChannels);
    try {
      final response = await http.get(Uri.parse('https://tinhlagi.pro/tivi/'));
      if (response.statusCode == 200) {
        final document = html_parser.parse(response.body);
        final headings = document.querySelectorAll('h2.group-title');
        
        for (var heading in headings) {
          String category = heading.text.trim();
          category = category.replaceAll(RegExp(r'\s*\(\d+\)$'), '').trim();
          
          final grid = heading.nextElementSibling;
          if (grid != null && grid.classes.contains('channel-grid')) {
            final aTags = grid.querySelectorAll('a.channel-card');
            
            for (var a in aTags) {
              final href = a.attributes['href'] ?? '';
              final uri = Uri.parse('https://tinhlagi.pro/tivi/' + href);
              String streamUrl = uri.queryParameters['url'] ?? '';
              final name = uri.queryParameters['name'] ?? a.querySelector('.channel-name')?.text.trim() ?? 'Unknown';
              final logo = a.querySelector('img')?.attributes['src'] ?? '';
              
              if (streamUrl.contains('youtube.com') || streamUrl.contains('youtu.be')) continue;
              
              String webUrl = '';
              if (streamUrl.contains('.mpd')) {
                webUrl = uri.toString();
                streamUrl = '';
              }
              
              String mappedCategory = category;
              if (category == '🌐| Thiết yếu' || category == 'LIVE EVENTS 🔴' || category.contains('In The Box')) {
                mappedCategory = 'Kênh Tổng Hợp';
              } else if (category == 'Quốc Tế' || category == 'Israel' || category == 'TVB') {
                mappedCategory = 'Kênh Quốc Tế';
              } else if (category == 'Địa phương') {
                mappedCategory = 'Kênh Địa Phương';
              } else if (category.contains('VTVcab')) {
                mappedCategory = 'VTVCab';
              } else if (category == 'ASEAN HUYNDAI CUP 2026') {
                mappedCategory = 'Kênh Thể Thao';
              }

              if ((streamUrl.isNotEmpty || webUrl.isNotEmpty)) {
                int existingIdx = channels.indexWhere((c) => (streamUrl.isNotEmpty && c.streamUrl == streamUrl) || c.name == name);
                if (existingIdx != -1) {
                  if (channels[existingIdx].logo.isEmpty && logo.isNotEmpty) {
                    channels[existingIdx] = channels[existingIdx].copyWith(logo: logo);
                  }
                } else {
                  channels.add(TvChannel(
                    id: 'tl_$name',
                    name: name,
                    category: mappedCategory,
                    logo: logo,
                    streamUrl: streamUrl,
                    webUrl: webUrl,
                  ));
                }
              }
            }
          }
        }
      }
    } catch (e) {
      // Ignored
    }
    
    return channels;
  }
}

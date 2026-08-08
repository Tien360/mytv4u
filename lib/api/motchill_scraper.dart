import 'package:html/parser.dart' as html_parser;
import 'package:html/dom.dart';
import 'package:http/http.dart' as http;
import '../models/movie.dart';

class MotchillScraper {
  static const String proxy = 'https://stream-proxy.oxaliplatin.workers.dev/?url=';
  static const String base = 'https://motchillv.biz';

  static Future<String?> _fetchHtml(String path) async {
    try {
      final fullPath = path.startsWith('http') ? path : (base + path);
      final url = '$proxy${Uri.encodeComponent(fullPath)}';
      final res = await http.get(Uri.parse(url)).timeout(const Duration(seconds: 8));
      if (res.statusCode == 200) {
        return res.body;
      }
    } catch (e) {
      // Handle error implicitly
    }
    return null;
  }

  static List<Movie> _parseMovies(Document doc) {
    final List<Movie> movies = [];
    final items = doc.querySelectorAll('.motchill-card, .myui-vodlist__box, .item');
    
    for (var el in items) {
      final aTag = el.querySelector('a');
      if (aTag == null) continue;
      
      final href = aTag.attributes['href'] ?? '';
      final match = RegExp(r'/phim/([^/]+)').firstMatch(href);
      if (match == null) continue;
      final slug = match.group(1)!;
      
      final img = el.querySelector('img');
      String name = aTag.attributes['title'] ?? el.querySelector('h3, h4')?.text.trim() ?? '';
      
      String thumb = img?.attributes['data-src'] ?? img?.attributes['src'] ?? '';
      if (thumb.isNotEmpty) {
        if (!thumb.startsWith('http')) {
          thumb = base + thumb;
        }
        if (!thumb.contains(proxy)) {
          thumb = proxy + Uri.encodeComponent(thumb);
        }
      }
      
      final currentEpisode = el.querySelector('.pic-text, .label, .mtc-chip--ep')?.text.trim() ?? '';
      String originalName = el.querySelector('.text.text-overflow, .name2, .mtc-movie-card__meta-origin')?.text.trim() ?? name;
      
      String quality = el.querySelector('.mtc-chip--sub, .mtc-chip--quality')?.text.trim() ?? '';
      String lang = '';
      if (quality == 'VIETSUB') {
        lang = 'Vietsub';
        quality = '';
      } else if (quality.contains(' - ')) {
        final parts = quality.split(' - ');
        quality = parts[0];
        if (parts.length > 1) lang = parts[1];
      }
      
      String year = el.querySelector('.mtc-movie-card__year-badge')?.text.trim() ?? '';
      
      movies.add(Movie(
        name: name,
        originalName: originalName,
        slug: slug,
        thumbUrl: thumb,
        posterUrl: thumb,
        currentEpisode: currentEpisode,
        quality: quality,
        language: lang,
        year: year,
        time: '',
        description: '',
        genres: [],
        countries: [],
        directors: [],
        casts: [],
        episodes: [],
        source: 'motchill',
      ));
    }
    return movies;
  }

  static Future<List<Movie>> getRecent(int page) async {
    final html = await _fetchHtml('/danh-sach/phim-moi?page=$page');
    if (html == null) return [];
    return _parseMovies(html_parser.parse(html));
  }

  static Future<List<Movie>> getByList(String slug, int page) async {
    final html = await _fetchHtml('/danh-sach/$slug?page=$page');
    if (html == null) return [];
    return _parseMovies(html_parser.parse(html));
  }

  static Future<List<Movie>> getByGenre(String slug, int page) async {
    final html = await _fetchHtml('/the-loai/$slug?page=$page');
    if (html == null) return [];
    return _parseMovies(html_parser.parse(html));
  }

  static Future<List<Movie>> getByCountry(String slug, int page) async {
    final html = await _fetchHtml('/quoc-gia/$slug?page=$page');
    if (html == null) return [];
    return _parseMovies(html_parser.parse(html));
  }

  static Future<List<Movie>> search(String keyword) async {
    final html = await _fetchHtml('/?search=${Uri.encodeComponent(keyword)}');
    if (html == null) return [];
    return _parseMovies(html_parser.parse(html));
  }

  static Future<Movie?> getDetail(String slug) async {
    final htmlStr = await _fetchHtml('/phim/$slug');
    if (htmlStr == null) return null;
    
    final doc = html_parser.parse(htmlStr);
    
    final name = doc.querySelector('h1')?.text.trim() ?? '';
    
    String originName = '';
    final originEl = doc.querySelector('.mtc-detail-hero__origin');
    if (originEl != null) {
      originName = originEl.text.split('\u00B7')[0].trim();
    }
    
    final img = doc.querySelector('.movie-l-img img, .mtc-detail-hero__poster img');
    String posterUrl = img?.attributes['src'] ?? '';
    if (posterUrl.isNotEmpty) {
      if (!posterUrl.startsWith('http')) {
        posterUrl = base + posterUrl;
      }
      if (!posterUrl.contains(proxy)) {
        posterUrl = proxy + Uri.encodeComponent(posterUrl);
      }
    }
    
    final description = doc.querySelector('.movie-detail-content, .mtc-detail-hero__synopsis, .mtc-detail-synopsis__content, .mtc-detail-synopsis')?.text.trim() ?? '';
    
    final episodeLinks = doc.querySelectorAll('.list-episode a, .mtc-detail-episodes__chip');
    final List<Episode> items = [];
    final seenEps = <String>{};
    
    for (var el in episodeLinks) {
      final epName = el.text.trim().isNotEmpty ? el.text.trim() : (el.attributes['title'] ?? '');
      final epHref = el.attributes['href'];
      
      if (epHref != null && epHref.contains('/tap-') && !seenEps.contains(epName)) {
        seenEps.add(epName);
        final relPath = epHref.replaceAll(base, '');
        items.add(Episode(
          name: epName,
          slug: epName.toLowerCase().replaceAll(' ', '-'),
          m3u8Url: 'motchill://$relPath', // Fix: Just use relPath since base is handled by _fetchHtml
          embedUrl: '',
        ));
      }
    }
    
    List<EpisodeServer> episodes = [];
    if (items.isNotEmpty) {
      try {
        final firstEpPath = items.first.m3u8Url.replaceFirst('motchill://', '');
        final htmlStr = await _fetchHtml(firstEpPath);
        if (htmlStr != null) {
          final docHtml = html_parser.parse(htmlStr);
          final subServers = _extractServersFromDoc(docHtml);
          
          if (subServers.isNotEmpty) {
            for (int i = 0; i < subServers.length; i++) {
              final svName = subServers[i]['name']!;
              final epList = items.map((e) => Episode(
                name: e.name,
                slug: e.slug,
                m3u8Url: '${e.m3u8Url}?sv=$i',
                embedUrl: '',
              )).toList();
              
              String displayName = 'Motchill ($svName)';
              if (svName.toLowerCase().contains('hls') || svName.toLowerCase().contains('m3u8')) {
                 displayName = 'Motchill #$i (HLS)';
              } else {
                 displayName = 'Motchill #$i (Embed)';
              }
              if (svName.toLowerCase().contains('vip')) displayName = 'Motchill - $svName';
              
              episodes.add(EpisodeServer(serverName: displayName, items: epList));
            }
          } else {
            episodes.add(EpisodeServer(serverName: 'Motchill Server', items: items));
          }
        } else {
          episodes.add(EpisodeServer(serverName: 'Motchill Server', items: items));
        }
      } catch (e) {
        episodes.add(EpisodeServer(serverName: 'Motchill Server', items: items));
      }
    }
    
    String year = '';
    String time = '';
    String quality = '';
    String lang = '';
    String episodeCurrent = '';
    List<String> genres = [];
    
    final statusItems = doc.querySelectorAll('.mtc-detail-meta-bar__item, .mtc-detail-meta-grid__item');
    for (var el in statusItems) {
      final text = el.text.replaceAll(RegExp(r'\s+'), ' ').trim();
      if (text.contains('Năm phát hành')) year = text.replaceAll(RegExp(r'.*Năm phát hành', caseSensitive: false), '').trim();
      else if (text.contains('Thời lượng')) time = text.replaceAll(RegExp(r'.*Thời lượng', caseSensitive: false), '').trim();
      else if (text.contains('Trạng thái')) episodeCurrent = text.replaceAll(RegExp(r'.*Trạng thái', caseSensitive: false), '').trim();
      else if (text.contains('Chất lượng')) quality = text.replaceAll(RegExp(r'.*Chất lượng', caseSensitive: false), '').trim();
      else if (text.contains('Ngôn ngữ')) lang = text.replaceAll(RegExp(r'.*Ngôn ngữ', caseSensitive: false), '').trim();
      else if (text.contains('Phụ đề') && lang == 'Vietsub') lang = 'Vietsub';
    }
    
    final genreLinks = doc.querySelectorAll('.mtc-detail-hero__categories a, .mtc-detail-hero__genres a, .mtc-detail-chip[href*="/the-loai/"]');
    for (var el in genreLinks) {
      final catName = el.text.trim();
      if (catName.isNotEmpty && !genres.contains(catName)) {
        genres.add(catName);
      }
    }
    if (genres.length > 5) genres = genres.sublist(0, 4);
    
    return Movie(
      name: name,
      originalName: originName,
      slug: slug,
      thumbUrl: posterUrl,
      posterUrl: posterUrl,
      currentEpisode: episodeCurrent,
      quality: quality,
      language: lang,
      year: year,
      time: time,
      description: description,
      genres: genres,
      countries: [],
      directors: [],
      casts: [],
      episodes: episodes,
      source: 'motchill',
    );
  }

  static Future<List<Map<String, String>>> getEpisodeServers(String motchillUrl) async {
    final path = motchillUrl.replaceFirst('motchill://', '');
    final htmlStr = await _fetchHtml(path);
    if (htmlStr == null) return [];
    
    final doc = html_parser.parse(htmlStr);
    List<Map<String, String>> servers = _extractServersFromDoc(doc);
    
    if (servers.isEmpty) {
      final m3u8Match = RegExp(r'(https:\/\/[^\s"''<>]+\.m3u8[^\s"''<>]*)', caseSensitive: false).firstMatch(htmlStr);
      if (m3u8Match != null) {
        servers.add({'name': 'Motchill Server (Fallback)', 'link': m3u8Match.group(1)!});
      }
    }
    
    return servers;
  }

  static List<Map<String, String>> _extractServersFromDoc(Document doc) {
    final buttons = doc.querySelectorAll('.streaming-server, [data-link]');
    List<Map<String, String>> servers = [];
    for (var btn in buttons) {
      String link = btn.attributes['data-link'] ?? btn.attributes['data-play'] ?? '';
      final name = btn.text.trim();
      
      if (link.isEmpty) continue;
      
      if (link.startsWith('//')) {
        link = 'https:$link';
      }
      
      final isM3u8 = link.contains('.m3u8');
      if (isM3u8 || link.contains('vevocloud') || link.contains('cloudbeta')) {
         link = 'https://stream-proxy.oxaliplatin.workers.dev/?url=${Uri.encodeComponent(link)}';
      }
      
      if (!servers.any((s) => s['link'] == link)) {
        servers.add({'name': name.isEmpty ? 'Server ${servers.length + 1}' : name, 'link': link});
      }
    }
    return servers;
  }
}

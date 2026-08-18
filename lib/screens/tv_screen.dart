import 'package:flutter/material.dart';
import '../api/tv_api.dart';
import '../models/movie.dart';
import 'player_screen.dart';
import 'tv_webview_screen.dart';
import '../widgets/glass_container.dart';

class TvScreen extends StatefulWidget {
  const TvScreen({Key? key}) : super(key: key);

  @override
  State<TvScreen> createState() => TvScreenState();
}

class TvScreenState extends State<TvScreen> {
  final ScrollController _categoryScrollController = ScrollController();
  List<TvChannel> _channels = [];
  bool _isLoading = true;
  String _selectedCategory = 'Tất cả';
  String _searchQuery = '';

  List<String> get _categories {
    final cats = _channels.map((c) => c.category).toSet().toList();
    cats.insert(0, 'Tất cả');
    return cats;
  }


  void performSearch(String query) {
    if (mounted) {
      setState(() {
        _searchQuery = query;
      });
    }
  }

  @override
  void dispose() {
    _categoryScrollController.dispose();
    super.dispose();
  }

  @override
  void initState() {
    super.initState();
    _loadChannels();
  }

  Future<void> _loadChannels() async {
    final channels = await TvApi.getChannels();
    if (mounted) {
      setState(() {
        _channels = channels;
        _isLoading = false;
      });
    }
  }

  List<TvChannel> get _filteredChannels {
    var list = _channels;
    if (_selectedCategory != 'Tất cả') {
      list = list.where((c) => c.category == _selectedCategory).toList();
    }
    if (_searchQuery.isNotEmpty) {
      list = list.where((c) => c.name.toLowerCase().contains(_searchQuery.toLowerCase())).toList();
    }
    return list;
  }

  void _playTvChannel(TvChannel channel) {
    if (channel.streamUrl.isEmpty && channel.webUrl.isNotEmpty) {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => TvWebViewScreen(
            title: channel.name,
            webUrl: channel.webUrl,
          ),
        ),
      );
      return;
    }

    final allTvEpisodes = _channels.map((c) => Episode(
      name: c.name,
      slug: c.id,
      embedUrl: c.streamUrl,
      m3u8Url: c.streamUrl,
    )).toList();

    final int initialIndex = allTvEpisodes.indexWhere((e) => e.slug == channel.id);

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => PlayerScreen(
          movieName: 'TV Live - ${channel.name}',
          episodes: allTvEpisodes,
          currentEpisodeIndex: initialIndex >= 0 ? initialIndex : 0,
          isLive: true,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,
      body: CustomScrollView(
        slivers: [
          // Header Banner in Electric Blue theme
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: const Color(0xFF3B82F6).withOpacity(0.2),
                          borderRadius: BorderRadius.circular(16),
                          border: Border.all(color: const Color(0xFF3B82F6).withOpacity(0.4)),
                        ),
                        child: const Icon(Icons.live_tv, color: Color(0xFF3B82F6), size: 28),
                      ),
                      const SizedBox(width: 14),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Kênh Truyền Hình TV Trực Tuyến',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 24,
                              fontWeight: FontWeight.bold,
                              letterSpacing: 0.5,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'Xem trực tiếp các kênh VTV, HTV, VTC, Truyền hình tỉnh chất lượng cao',
                            style: TextStyle(
                              color: Colors.white.withOpacity(0.6),
                              fontSize: 14,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                  const SizedBox(height: 24),
                  
                  // Category Filter Pills in Electric Blue
                  Row(
                      children: [
                        IconButton(
                          icon: const Icon(Icons.chevron_left, color: Colors.white54),
                          onPressed: () {
                            _categoryScrollController.animateTo(
                              _categoryScrollController.offset - 200,
                              duration: const Duration(milliseconds: 300),
                              curve: Curves.easeInOut,
                            );
                          },
                        ),
                        Expanded(
                          child: SingleChildScrollView(
                            controller: _categoryScrollController,
                            scrollDirection: Axis.horizontal,
                            child: Row(
                              children: _categories.map((cat) {
                        final isSelected = _selectedCategory == cat;
                        return Padding(
                          padding: const EdgeInsets.only(right: 12.0),
                          child: InkWell(
                            onTap: () => setState(() => _selectedCategory = cat),
                            borderRadius: BorderRadius.circular(20),
                            child: AnimatedContainer(
                              duration: const Duration(milliseconds: 200),
                              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                              decoration: BoxDecoration(
                                color: isSelected 
                                    ? const Color(0xFF3B82F6) 
                                    : Colors.white.withOpacity(0.08),
                                borderRadius: BorderRadius.circular(20),
                                border: Border.all(
                                  color: isSelected ? const Color(0xFF3B82F6) : Colors.white12,
                                  width: 1,
                                ),
                                boxShadow: isSelected
                                    ? [
                                        BoxShadow(
                                          color: const Color(0xFF3B82F6).withOpacity(0.4),
                                          blurRadius: 10,
                                          spreadRadius: 1,
                                        )
                                      ]
                                    : [],
                              ),
                              child: Text(
                                cat,
                                style: TextStyle(
                                  color: isSelected ? Colors.white : Colors.white70,
                                  fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
                                  fontSize: 14,
                                ),
                              ),
                            ),
                          ),
                        );
                      }).toList(),
                            ),
                          ),
                        ),
                        IconButton(
                          icon: const Icon(Icons.chevron_right, color: Colors.white54),
                          onPressed: () {
                            _categoryScrollController.animateTo(
                              _categoryScrollController.offset + 200,
                              duration: const Duration(milliseconds: 300),
                              curve: Curves.easeInOut,
                            );
                          },
                        ),
                      ],
                    ),
                ],
              ),
            ),
          ),

          // Channel Grid
          if (_isLoading)
            const SliverFillRemaining(
              child: Center(
                child: CircularProgressIndicator(color: Color(0xFF3B82F6)),
              ),
            )
          else if (_filteredChannels.isEmpty)
            SliverFillRemaining(
              child: Center(
                child: Text(
                  'Không tìm thấy kênh truyền hình nào',
                  style: TextStyle(color: Colors.white.withOpacity(0.6), fontSize: 16),
                ),
              ),
            )
          else
            SliverPadding(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
              sliver: SliverGrid(
                gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
                  maxCrossAxisExtent: 220,
                  mainAxisSpacing: 18,
                  crossAxisSpacing: 18,
                  childAspectRatio: 1.1,
                ),
                delegate: SliverChildBuilderDelegate(
                  (context, index) {
                    final channel = _filteredChannels[index];
                    return _TvChannelCard(
                      channel: channel,
                      onTap: () => _playTvChannel(channel),
                    );
                  },
                  childCount: _filteredChannels.length,
                ),
              ),
            ),
        ],
      ),
    );
  }
}

class _TvChannelCard extends StatefulWidget {
  final TvChannel channel;
  final VoidCallback onTap;

  const _TvChannelCard({
    Key? key,
    required this.channel,
    required this.onTap,
  }) : super(key: key);

  @override
  State<_TvChannelCard> createState() => _TvChannelCardState();
}

class _TvChannelCardState extends State<_TvChannelCard> {
  bool _isHovered = false;

  Widget _buildChannelLogo() {
    final id = widget.channel.id.toLowerCase();
    
    // Custom High-Quality Branded Badges for each TV station
    if (id.contains('thvl') || id.contains('vinhlong')) {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            colors: [Color(0xFF059669), Color(0xFF0284C7)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(12),
          boxShadow: [BoxShadow(color: Colors.green.withOpacity(0.3), blurRadius: 8)],
        ),
        child: Text(widget.channel.name, style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.w900, fontStyle: FontStyle.italic)),
      );
    } else if (id.contains('vtv')) {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            colors: [Color(0xFFDC2626), Color(0xFF2563EB)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(12),
          boxShadow: [BoxShadow(color: Colors.red.withOpacity(0.3), blurRadius: 8)],
        ),
        child: Text(widget.channel.name, style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.w900, fontStyle: FontStyle.italic)),
      );
    } else if (id.contains('htv7')) {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            colors: [Color(0xFFE11D48), Color(0xFFF59E0B)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(12),
          boxShadow: [BoxShadow(color: Colors.red.withOpacity(0.3), blurRadius: 8)],
        ),
        child: Text('HTV 7', style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.w900, fontStyle: FontStyle.italic)),
      );
    } else if (id.contains('htv9')) {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            colors: [Color(0xFF2563EB), Color(0xFFDC2626)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(12),
          boxShadow: [BoxShadow(color: Colors.blue.withOpacity(0.3), blurRadius: 8)],
        ),
        child: Text('HTV 9', style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.w900, fontStyle: FontStyle.italic)),
      );
    } else if (id.contains('antv')) {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            colors: [Color(0xFFD97706), Color(0xFF991B1B)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(12),
          boxShadow: [BoxShadow(color: Colors.amber.withOpacity(0.3), blurRadius: 8)],
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: const [
            Icon(Icons.shield, color: Colors.amberAccent, size: 20),
            SizedBox(width: 6),
            Text('ANTV', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
          ],
        ),
      );
    } else if (id.contains('qpvn')) {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            colors: [Color(0xFF15803D), Color(0xFF047857)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(12),
          boxShadow: [BoxShadow(color: Colors.green.withOpacity(0.3), blurRadius: 8)],
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: const [
            Icon(Icons.star, color: Colors.amberAccent, size: 20),
            SizedBox(width: 6),
            Text('QPVN', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
          ],
        ),
      );
    } else if (id.contains('tvb')) {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            colors: [Color(0xFF9333EA), Color(0xFF4F46E5)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(12),
          boxShadow: [BoxShadow(color: Colors.purple.withOpacity(0.3), blurRadius: 8)],
        ),
        child: Text('TVB VIETNAM', style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
      );
    } else if (id.contains('sctv')) {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            colors: [Color(0xFF0284C7), Color(0xFF2563EB)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Text(widget.channel.name, style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
      );
    } else if (id.contains('hanoi') || id.contains('hn1')) {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            colors: [Color(0xFF0284C7), Color(0xFF0D9488)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Text('HÀ NỘI 1', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
      );
    } else if (id.contains('dongthap')) {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            colors: [Color(0xFF059669), Color(0xFF0284C7)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Text('ĐỒNG THÁP', style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
      );
    } else if (id.contains('cantho')) {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            colors: [Color(0xFF4F46E5), Color(0xFF9333EA)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Text(widget.channel.name, style: const TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.bold)),
      );
    }

    // Default Fallback Branded Pill
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: const Color(0xFF3B82F6).withOpacity(0.2),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFF3B82F6).withOpacity(0.4)),
      ),
      child: Text(
        widget.channel.name,
        style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
        textAlign: TextAlign.center,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      onEnter: (_) => setState(() => _isHovered = true),
      onExit: (_) => setState(() => _isHovered = false),
      child: GestureDetector(
        onTap: widget.onTap,
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 200),
          transform: Matrix4.identity()..scale(_isHovered ? 1.04 : 1.0),
          decoration: BoxDecoration(
            color: _isHovered ? Colors.white.withOpacity(0.12) : Colors.white.withOpacity(0.05),
            borderRadius: BorderRadius.circular(16),
            border: Border.all(
              color: _isHovered ? const Color(0xFF3B82F6) : Colors.white12,
              width: _isHovered ? 1.5 : 1,
            ),
            boxShadow: _isHovered
                ? [
                    BoxShadow(
                      color: const Color(0xFF3B82F6).withOpacity(0.3),
                      blurRadius: 16,
                      spreadRadius: 2,
                    )
                  ]
                : [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.4),
                      blurRadius: 8,
                    )
                  ],
          ),
          child: Padding(
            padding: const EdgeInsets.all(14.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // LIVE Badge
                Align(
                  alignment: Alignment.topRight,
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                    decoration: BoxDecoration(
                      color: const Color(0xFFEF4444),
                      borderRadius: BorderRadius.circular(10),
                      boxShadow: [
                        BoxShadow(
                          color: const Color(0xFFEF4444).withOpacity(0.4),
                          blurRadius: 6,
                        ),
                      ],
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: const [
                        Icon(Icons.circle, color: Colors.white, size: 6),
                        SizedBox(width: 4),
                        Text(
                          'LIVE',
                          style: TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 4),

                // Channel Logo Badge
                Expanded(
                  child: Center(
                    child: _buildChannelLogo(),
                  ),
                ),
                const SizedBox(height: 8),

                // Channel Name
                Text(
                  widget.channel.name,
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 13,
                    fontWeight: FontWeight.bold,
                    shadows: _isHovered
                        ? [const Shadow(color: Color(0xFF3B82F6), blurRadius: 8)]
                        : [],
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

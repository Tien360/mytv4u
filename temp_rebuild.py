import sys

with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    code = f.read()

# We need to replace the entire build method.
# Find the start of the build method
start_idx = code.find("  @override\n  Widget build(BuildContext context) {")
if start_idx == -1:
    print("Could not find build method")
    sys.exit(1)

# Find the end of the build method (the next method is usually _buildBadgeIcon or _buildInfoRow)
end_idx = code.find("  Widget _buildBadgeIcon(", start_idx)
if end_idx == -1:
    print("Could not find end of build method")
    sys.exit(1)

new_build = """  @override
  Widget build(BuildContext context) {
    if (_movie == null) {
      return const Scaffold(
        backgroundColor: Colors.black,
        body: Center(
          child: CircularProgressIndicator(color: Colors.amber),
        ),
      );
    }

    final screenHeight = MediaQuery.of(context).size.height;
    bool hasBackdrop = _movie!.posterUrl.isNotEmpty;
    String heroImage = hasBackdrop ? _movie!.posterUrl : _movie!.thumbUrl;

    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          // 1. Full Screen Background Image (NO HERO TAG to prevent crashes during transition)
          Positioned.fill(
            child: CachedNetworkImage(
              imageUrl: heroImage,
              fit: BoxFit.cover,
              alignment: Alignment.topCenter,
            ),
          ),

          // 2. Stepped Gradient Blur (Safe for Windows)
          // We blur the bottom 60% of the screen. The top 40% is clear.
          // We use 4 steps to create a smooth transition.
          Positioned.fill(
            child: LayoutBuilder(
              builder: (context, constraints) {
                final startY = constraints.maxHeight * 0.35; // Start blurring at 35% height
                final endY = constraints.maxHeight * 0.5;   // Fully blurred at 50% height
                final steps = 4;
                final stepHeight = (endY - startY) / steps;
                final maxBlur = 12.0;

                List<Widget> blurLayers = [];
                
                // Transitional blur strips
                for (int i = 0; i < steps; i++) {
                  final double currentBlur = (maxBlur / steps) * (i + 1);
                  blurLayers.add(
                    Positioned(
                      top: startY + (i * stepHeight),
                      height: stepHeight,
                      left: 0,
                      right: 0,
                      child: ClipRect(
                        child: BackdropFilter(
                          filter: ImageFilter.blur(sigmaX: currentBlur, sigmaY: currentBlur),
                          child: const SizedBox.expand(),
                        ),
                      ),
                    ),
                  );
                }
                
                // Solid blur for the rest of the screen
                blurLayers.add(
                  Positioned(
                    top: endY,
                    bottom: 0,
                    left: 0,
                    right: 0,
                    child: ClipRect(
                      child: BackdropFilter(
                        filter: ImageFilter.blur(sigmaX: maxBlur, sigmaY: maxBlur),
                        child: const SizedBox.expand(),
                      ),
                    ),
                  ),
                );

                return Stack(children: blurLayers);
              },
            ),
          ),

          // 3. Dark Gradient Overlay for Text Readability
          Positioned.fill(
            child: Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [
                    Colors.black.withOpacity(0.0),
                    Colors.black.withOpacity(0.6),
                    Colors.black.withOpacity(0.9),
                    Colors.black,
                  ],
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  stops: const [0.2, 0.5, 0.8, 1.0],
                ),
              ),
            ),
          ),

          // 4. Webview for Inline Trailer (if applicable)
          if (_showInlineTrailer && _isWebviewInitialized)
            Positioned.fill(
              child: Webview(_webviewController),
            ),

          // 5. Scrollable Content
          CustomScrollView(
            slivers: [
              // Top padding to push content down
              SliverToBoxAdapter(
                child: SizedBox(height: screenHeight * 0.4),
              ),
              
              // Main Content Area
              SliverToBoxAdapter(
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 40.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Header Row: Title & Badges
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.end,
                        children: [
                          if (!hasBackdrop) ...[
                            ClipRRect(
                              borderRadius: BorderRadius.circular(12),
                              child: Hero(
                                tag: widget.heroTag ?? widget.slug,
                                child: CachedNetworkImage(
                                  imageUrl: _movie!.thumbUrl,
                                  width: 160,
                                  height: 240,
                                  fit: BoxFit.cover,
                                ),
                              ),
                            ),
                            const SizedBox(width: 24),
                          ],
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  '${_movie!.name} (\U0001f9ea Bản Test)',
                                  style: const TextStyle(
                                    fontSize: 48,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.white,
                                    height: 1.1,
                                    shadows: [
                                      Shadow(
                                        color: Colors.black54,
                                        blurRadius: 10,
                                        offset: Offset(0, 4),
                                      ),
                                    ],
                                  ),
                                ),
                                const SizedBox(height: 8),
                                Text(
                                  _movie!.originName,
                                  style: TextStyle(
                                    fontSize: 24,
                                    color: Colors.white.withOpacity(0.7),
                                    fontStyle: FontStyle.italic,
                                  ),
                                ),
                                const SizedBox(height: 24),
                                // Badges
                                Row(
                                  children: [
                                    _buildBadgeIcon(Icons.calendar_today, _movie!.year.toString()),
                                    const SizedBox(width: 16),
                                    _buildBadgeIcon(Icons.access_time, _movie!.time),
                                    const SizedBox(width: 16),
                                    _buildBadgeIcon(Icons.high_quality, _movie!.quality),
                                    const SizedBox(width: 16),
                                    _buildBadgeIcon(Icons.subtitles, _movie!.lang),
                                    const SizedBox(width: 16),
                                    if (_movie!.episodeCurrent.isNotEmpty)
                                      Container(
                                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                        decoration: BoxDecoration(
                                          color: Colors.amber.withOpacity(0.2),
                                          borderRadius: BorderRadius.circular(20),
                                          border: Border.all(color: Colors.amber.withOpacity(0.5)),
                                        ),
                                        child: Text(
                                          _movie!.episodeCurrent,
                                          style: const TextStyle(
                                            color: Colors.amber,
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                      ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                      
                      const SizedBox(height: 40),
                      
                      // Action Buttons & Info
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          // Left Column: Play Button & Overview
                          Expanded(
                            flex: 2,
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                // Action Buttons
                                Row(
                                  children: [
                                    ElevatedButton.icon(
                                      onPressed: () {
                                        Navigator.push(
                                          context,
                                          MaterialPageRoute(
                                            builder: (context) => PlayerScreen(
                                              movie: _movie!,
                                              episodeSlug: '',
                                              serverName: '',
                                            ),
                                          ),
                                        );
                                      },
                                      icon: const Icon(Icons.play_arrow_rounded, size: 32),
                                      label: const Text(
                                        'XEM PHIM',
                                        style: TextStyle(
                                          fontSize: 18,
                                          fontWeight: FontWeight.bold,
                                          letterSpacing: 1.2,
                                        ),
                                      ),
                                      style: ElevatedButton.styleFrom(
                                        foregroundColor: Colors.black,
                                        backgroundColor: Colors.amber,
                                        padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 20),
                                        shape: RoundedRectangleBorder(
                                          borderRadius: BorderRadius.circular(30),
                                        ),
                                        elevation: 8,
                                      ),
                                    ),
                                    const SizedBox(width: 16),
                                    if (_movie!.trailerUrl.isNotEmpty)
                                      OutlinedButton.icon(
                                        onPressed: () {
                                          if (!_isWebviewInitialized) {
                                            _initWebview();
                                          }
                                          setState(() {
                                            _showInlineTrailer = !_showInlineTrailer;
                                            _trailerEnded = false;
                                          });
                                          if (_showInlineTrailer) {
                                            _webviewController.loadUrl(_movie!.trailerUrl);
                                          } else {
                                            _webviewController.loadUrl('about:blank');
                                          }
                                        },
                                        icon: Icon(_showInlineTrailer ? Icons.close : Icons.movie_creation_outlined),
                                        label: Text(_showInlineTrailer ? 'ĐÓNG TRAILER' : 'TRAILER'),
                                        style: OutlinedButton.styleFrom(
                                          foregroundColor: Colors.white,
                                          side: const BorderSide(color: Colors.white54, width: 2),
                                          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
                                          shape: RoundedRectangleBorder(
                                            borderRadius: BorderRadius.circular(30),
                                          ),
                                        ),
                                      ),
                                  ],
                                ),
                                const SizedBox(height: 40),
                                
                                // Overview
                                const Text(
                                  'NỘI DUNG PHIM',
                                  style: TextStyle(
                                    fontSize: 20,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.white,
                                    letterSpacing: 1.2,
                                  ),
                                ),
                                const SizedBox(height: 16),
                                Text(
                                  _movie!.content,
                                  style: const TextStyle(
                                    fontSize: 16,
                                    color: Colors.white70,
                                    height: 1.6,
                                  ),
                                ),
                              ],
                            ),
                          ),
                          
                          const SizedBox(width: 60),
                          
                          // Right Column: Metadata
                          Expanded(
                            flex: 1,
                            child: GlassContainer(
                              padding: const EdgeInsets.all(24),
                              borderRadius: BorderRadius.circular(20),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  _buildInfoRow('Trạng thái', _movie!.status == 'completed' ? 'Hoàn tất' : 'Đang chiếu'),
                                  _buildDivider(),
                                  _buildInfoRow('Quốc gia', _movie!.country.map((e) => e.name).join(', ')),
                                  _buildDivider(),
                                  _buildInfoRow('Thể loại', _movie!.category.map((e) => e.name).join(', ')),
                                  _buildDivider(),
                                  _buildInfoRow('Đạo diễn', _movie!.director.join(', ')),
                                  _buildDivider(),
                                  _buildInfoRow('Diễn viên', _movie!.actor.join(', ')),
                                ],
                              ),
                            ),
                          ),
                        ],
                      ),
                      
                      const SizedBox(height: 60),
                      
                      // Episodes Section (if any)
                      if (_movie!.episodes.isNotEmpty && _movie!.episodes.first.serverData.isNotEmpty) ...[
                        const Text(
                          'CHỌN TẬP',
                          style: TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                            letterSpacing: 1.2,
                          ),
                        ),
                        const SizedBox(height: 24),
                        // Render episodes here... we will use a simple Wrap for now
                        Wrap(
                          spacing: 12,
                          runSpacing: 12,
                          children: _movie!.episodes.first.serverData.map((ep) {
                            return InkWell(
                              onTap: () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (context) => PlayerScreen(
                                      movie: _movie!,
                                      episodeSlug: ep.slug,
                                      serverName: _movie!.episodes.first.serverName,
                                    ),
                                  ),
                                );
                              },
                              borderRadius: BorderRadius.circular(8),
                              child: Container(
                                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                                decoration: BoxDecoration(
                                  color: Colors.white.withOpacity(0.1),
                                  borderRadius: BorderRadius.circular(8),
                                  border: Border.all(color: Colors.white.withOpacity(0.2)),
                                ),
                                child: Text(
                                  ep.name,
                                  style: const TextStyle(
                                    color: Colors.white,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                            );
                          }).toList(),
                        ),
                        const SizedBox(height: 60),
                      ],
                    ],
                  ),
                ),
              ),
            ],
          ),
          
          // 6. Back Button
          Positioned(
            top: 40,
            left: 40,
            child: IconButton(
              icon: const Icon(Icons.arrow_back_ios_new, color: Colors.white, size: 28),
              onPressed: () => Navigator.pop(context),
            ),
          ),
        ],
      ),
    );
  }
"""

code = code[:start_idx] + new_build + code[end_idx:]

# Import ui for ImageFilter
if "import 'dart:ui';" not in code:
    code = "import 'dart:ui';\n" + code

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(code)
    
print("Updated movie_detail_screen_test.dart with safe stepped blur and no Hero background.")

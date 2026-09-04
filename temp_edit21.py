import re

with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

if "package:palette_generator/palette_generator.dart" not in c:
    c = c.replace("import 'package:flutter/material.dart';", 
                  "import 'package:flutter/material.dart';\nimport 'package:palette_generator/palette_generator.dart';\nimport 'package:cached_network_image/cached_network_image.dart';")

if "_dominantColor" not in c:
    c = re.sub(r'(class _MovieDetailScreenTestState extends State<MovieDetailScreenTest> \{[\s\S]*?)(bool _isLoading = true;)',
               r'\1\2\n  Color _dominantColor = Colors.redAccent;\n  final Map<String, double> _episodeProgressMap = {};',
               c)

if "_loadEpisodeProgressAndColor" not in c:
    func = """
  Future<void> _loadEpisodeProgressAndColor() async {
    if (_movie != null && _movie!.thumbUrl.isNotEmpty) {
      try {
        final PaletteGenerator paletteGenerator = await PaletteGenerator.fromImageProvider(
          CachedNetworkImageProvider(_movie!.thumbUrl),
          maximumColorCount: 20,
        );
        if (mounted) {
          setState(() {
            _dominantColor = paletteGenerator.vibrantColor?.color ?? 
                             paletteGenerator.dominantColor?.color ?? 
                             Colors.redAccent;
          });
        }
      } catch (e) {}
    }

    if (_movie == null) return;
    final prefs = await SharedPreferences.getInstance();
    final keys = prefs.getKeys();
    final prefix = 'continue_${_movie!.name}_';
    final durationPrefix = 'continue_duration_${_movie!.name}_';

    if (mounted) {
      setState(() {
        for (var key in keys) {
          if (key.startsWith(prefix)) {
            final epName = key.substring(prefix.length);
            final posMs = prefs.getInt(key) ?? 0;
            final durKey = durationPrefix + epName;
            final durMs = prefs.getInt(durKey) ?? 0;
            
            if (posMs > 0) {
              double fraction = 0.05;
              if (durMs > 0) {
                fraction = (posMs / durMs).clamp(0.0, 1.0);
              }
              if (fraction > 0 && fraction < 0.05) fraction = 0.05;
              _episodeProgressMap[epName] = fraction;
            }
          }
        }
      });
    }
  }
"""
    c = c.replace("void _fetchDetail() {", func + "\n  void _fetchDetail() {")

# Call it in _fetchDetail
c = c.replace("_isLoading = false;\n              });\n              _categorizeServers", 
              "_isLoading = false;\n              });\n              _loadEpisodeProgressAndColor();\n              _categorizeServers")

# HoverEpisodeButton updates
old_btn = """class HoverEpisodeButton extends StatefulWidget {
  final String text;
  final VoidCallback onTap;

  const HoverEpisodeButton({
    super.key,
    required this.text,
    required this.onTap,
  });"""
new_btn = """class HoverEpisodeButton extends StatefulWidget {
  final String text;
  final VoidCallback onTap;
  final double progress;
  final Color progressColor;

  const HoverEpisodeButton({
    super.key,
    required this.text,
    required this.onTap,
    this.progress = 0.0,
    this.progressColor = Colors.redAccent,
  });"""
c = c.replace(old_btn, new_btn)

# Stack in HoverEpisodeButton
old_stack = """            children: [
              isMinimalistUi.value 
                ? AnimatedContainer("""
new_stack = """            children: [
              isMinimalistUi.value 
                ? AnimatedContainer("""
if "if (widget.progress > 0)" not in c:
    c = c.replace("""                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );""", """                  ),
                ),
              ),
            ),
              if (widget.progress > 0)
                Positioned(
                  bottom: 0, left: 0, right: 0,
                  child: Container(
                    height: 3,
                    alignment: Alignment.centerLeft,
                    child: FractionallySizedBox(
                      widthFactor: widget.progress.clamp(0.0, 1.0),
                      child: Container(color: widget.progressColor),
                    ),
                  ),
                ),
          ),
        ),
      ),
    );""")

# HoverEpisodeButton usages
c = re.sub(r'return HoverEpisodeButton\(\s*text: dispName,\s*onTap: \(\) async \{', 
           r'return HoverEpisodeButton(\n                text: dispName,\n                progress: _episodeProgressMap[ep.name] ?? 0.0,\n                progressColor: _dominantColor,\n                onTap: () async {', c)

c = re.sub(r'return HoverEpisodeButton\(\s*text: stream.name,\s*onTap: \(\) async \{', 
           r'return HoverEpisodeButton(\n                text: stream.name,\n                progress: _episodeProgressMap[\'${_selectedP2pEpisode!.slug} - ${stream.name}\'] ?? 0.0,\n                progressColor: _dominantColor,\n                onTap: () async {', c)

# Await Navigator.push and reload
c = re.sub(r'Navigator\.push\(\s*context,\s*MaterialPageRoute\(\s*builder: \(_\) => PlayerScreen\(.*?\),\s*\),\s*\);',
           r'await Navigator.push(\g<0>);\n                  _loadEpisodeProgressAndColor();', c)
c = c.replace("await await Navigator.push", "await Navigator.push") # just in case

# P2P UI update
old_p2p = """                      child: Text(
                        ep.name,
                        style: TextStyle(color: isActive ? Colors.white : Colors.white70),
                      ),
                    ),"""
new_p2p = """                      child: Text(
                        ep.name,
                        style: TextStyle(color: isActive ? Colors.white : Colors.white70),
                      ),
                    ),
                    if ((_episodeProgressMap[ep.name] ?? 0.0) > 0)
                      Positioned(
                        bottom: 0, left: 0, right: 0,
                        child: Container(
                          height: 3,
                          alignment: Alignment.centerLeft,
                          child: FractionallySizedBox(
                            widthFactor: (_episodeProgressMap[ep.name] ?? 0.0).clamp(0.0, 1.0),
                            child: Container(color: _dominantColor),
                          ),
                        ),
                      ),"""
if "FractionallySizedBox" not in c.split("child: Text(\n                        ep.name,")[1][:500]:
    c = c.replace(old_p2p, new_p2p)

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Injected progress UI into movie_detail_screen_test.dart")

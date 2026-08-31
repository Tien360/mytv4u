import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/gaming_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = """              itemBuilder: (context, index) {
                final game = _games[index];
                return GestureDetector(
                  onTap: () => _onGameTap(game['url']!, game['title']!),
                  child: GlassContainer(
                    borderRadius: 16,
                    padding: const EdgeInsets.all(0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Expanded(
                          child: ClipRRect(
                            borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
                            child: Image.network(
                              game['image']!,
                              fit: BoxFit.cover,
                            ),
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.all(12),
                          color: Colors.black45,
                          child: Text(
                            game['title']!,
                            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
                            textAlign: TextAlign.center,
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              },"""

new_logic = """              itemBuilder: (context, index) {
                final game = _games[index];
                return _GameCard(
                  game: game,
                  onTap: () => _onGameTap(game['url']!, game['title']!),
                );
              },"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    
    # Add _GameCard class at the end
    content += """
class _GameCard extends StatefulWidget {
  final Map<String, String> game;
  final VoidCallback onTap;
  
  const _GameCard({Key? key, required this.game, required this.onTap}) : super(key: key);

  @override
  State<_GameCard> createState() => _GameCardState();
}

class _GameCardState extends State<_GameCard> {
  bool _isHovered = false;

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      onEnter: (_) => setState(() => _isHovered = true),
      onExit: (_) => setState(() => _isHovered = false),
      cursor: SystemMouseCursors.click,
      child: GestureDetector(
        onTap: widget.onTap,
        child: AnimatedScale(
          scale: _isHovered ? 1.05 : 1.0,
          duration: const Duration(milliseconds: 200),
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 200),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(16),
              boxShadow: _isHovered
                  ? [BoxShadow(color: Colors.blueAccent.withOpacity(0.5), blurRadius: 15, spreadRadius: 2)]
                  : [],
            ),
            child: GlassContainer(
              borderRadius: 16,
              padding: const EdgeInsets.all(0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Expanded(
                    child: ClipRRect(
                      borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
                      child: Image.network(
                        widget.game['image']!,
                        fit: BoxFit.cover,
                      ),
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.all(12),
                    color: _isHovered ? Colors.blueAccent.withOpacity(0.8) : Colors.black45,
                    child: Text(
                      widget.game['title']!,
                      style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
                      textAlign: TextAlign.center,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
"""
    with open('lib/screens/gaming_screen.dart', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added hover effect to GameCard")
else:
    print("Could not find old_logic")

import re

with open("lib/screens/sport_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

# I will replace the `_buildMatchCard` method with a more professional design.
new_method = """  Widget _buildMatchCard(SportMatch match) {
    final isLive = match.status.toLowerCase() == 'live';
    
    // Parse teams
    String teamHome = '';
    String teamAway = '';
    bool hasVs = false;
    
    if (match.title.toLowerCase().contains(' vs ')) {
      final parts = match.title.split(RegExp(r'(?i) vs '));
      if (parts.length >= 2) {
        teamHome = parts[0].trim();
        teamAway = parts[1].trim();
        hasVs = true;
      }
    }

    return GlassContainer(
      borderRadius: 16,
      child: InkWell(
        borderRadius: BorderRadius.circular(16),
        onTap: () => _playMatch(match),
        child: Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(16),
            border: Border.all(
              color: isLive ? Colors.redAccent.withValues(alpha: 0.3) : Colors.white10,
              width: 1,
            ),
            gradient: isLive ? LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [
                Colors.redAccent.withValues(alpha: 0.05),
                Colors.transparent,
              ]
            ) : null,
          ),
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // Header: League & Status
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Text(
                      match.league,
                      style: const TextStyle(
                        color: Colors.white70,
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                  if (isLive)
                    Row(
                      children: [
                        Container(
                          width: 8,
                          height: 8,
                          decoration: const BoxDecoration(
                            color: Colors.redAccent,
                            shape: BoxShape.circle,
                          ),
                        ),
                        const SizedBox(width: 4),
                        const Text(
                          'LIVE',
                          style: TextStyle(
                            color: Colors.redAccent,
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    )
                  else
                    Text(
                      match.time,
                      style: const TextStyle(
                        color: Colors.blueAccent,
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                ],
              ),
              const Spacer(),
              
              // Teams
              if (hasVs)
                Row(
                  children: [
                    Expanded(
                      flex: 4,
                      child: Text(
                        teamHome,
                        textAlign: TextAlign.right,
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    const Expanded(
                      flex: 2,
                      child: Center(
                        child: Text(
                          'VS',
                          style: TextStyle(
                            color: Colors.white30,
                            fontSize: 14,
                            fontWeight: FontWeight.w900,
                            fontStyle: FontStyle.italic,
                          ),
                        ),
                      ),
                    ),
                    Expanded(
                      flex: 4,
                      child: Text(
                        teamAway,
                        textAlign: TextAlign.left,
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  ],
                )
              else
                Text(
                  match.title,
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                
              const Spacer(),
              
              // Footer: Sources
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    match.sources.isNotEmpty ? Icons.play_circle_fill : Icons.block,
                    color: match.sources.isNotEmpty ? Colors.white54 : Colors.redAccent.withValues(alpha: 0.5),
                    size: 14,
                  ),
                  const SizedBox(width: 4),
                  Text(
                    match.sources.isNotEmpty 
                        ? '${match.sources.length} Nguồn phát'
                        : 'Chưa có nguồn',
                    style: TextStyle(
                      color: match.sources.isNotEmpty ? Colors.white54 : Colors.redAccent.withValues(alpha: 0.5), 
                      fontSize: 12,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }"""

text = re.sub(r'  Widget _buildMatchCard\(SportMatch match\) \{.*?(?=\n\}\n\nclass SportLivescoreWidget)/s', new_method, text, flags=re.DOTALL)

with open("lib/screens/sport_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated _buildMatchCard!")

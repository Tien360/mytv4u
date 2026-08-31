def add_thumbnails(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    target = '''child: Text(
                                            ep.name,
                                            style: TextStyle(
                                              color: isCurrent
                                                  ? Colors.blueAccent
                                                  : Colors.white,
                                              fontWeight: isCurrent
                                                  ? FontWeight.bold
                                                  : FontWeight.normal,
                                            ),
                                          ),'''
    
    replacement = '''child: Row(
                                            children: [
                                              if (ep.embedUrl.startsWith('https://i.ytimg.com/')) ...[
                                                ClipRRect(
                                                  borderRadius: BorderRadius.circular(6),
                                                  child: Image.network(
                                                    ep.embedUrl,
                                                    width: 100,
                                                    height: 56,
                                                    fit: BoxFit.cover,
                                                    errorBuilder: (context, error, stackTrace) => const SizedBox(width: 100, height: 56, child: Icon(Icons.error, color: Colors.white30)),
                                                  ),
                                                ),
                                                const SizedBox(width: 12),
                                              ],
                                              Expanded(
                                                child: Text(
                                                  ep.name,
                                                  style: TextStyle(
                                                    color: isCurrent
                                                        ? Colors.blueAccent
                                                        : Colors.white,
                                                    fontWeight: isCurrent
                                                        ? FontWeight.bold
                                                        : FontWeight.normal,
                                                    height: 1.3,
                                                  ),
                                                  maxLines: 2,
                                                  overflow: TextOverflow.ellipsis,
                                                ),
                                              ),
                                            ],
                                          ),'''
    
    content = content.replace(target, replacement)
    
    # Also fix the padding for the thumbnail container so it's not too wide
    content = content.replace('''padding: const EdgeInsets.symmetric(
                                            horizontal: 16,
                                            vertical: 10,
                                          ),''', '''padding: const EdgeInsets.symmetric(
                                            horizontal: 12,
                                            vertical: 8,
                                          ),''')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

add_thumbnails('lib/screens/player_screen.dart')
print("Added thumbnails")

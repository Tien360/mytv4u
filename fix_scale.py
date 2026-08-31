import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

old_expanded = '''                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 32.0),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        // Artwork / Vinyl
                        Hero(
                          tag: 'artwork',
                          child: isPodcast
                              ? Container(
                                  width: 300,
                                  height: 300,
                                  decoration: BoxDecoration(
                                    color: Colors.grey[800],
                                    borderRadius: BorderRadius.circular(24),
                                    boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 30, offset: Offset(0, 15))],
                                  ),
                                  child: const Icon(Icons.podcasts, size: 120, color: Colors.blueAccent),
                                )
                              : AnimatedBuilder(
                                  animation: _spinController,
                                  builder: (_, child) {
                                    return Transform.rotate(
                                      angle: _spinController.value * 2 * math.pi,
                                      child: child,
                                    );
                                  },
                                  child: Container(
                                    width: 320,
                                    height: 320,
                                    decoration: BoxDecoration(
                                      shape: BoxShape.circle,
                                      color: const Color(0xFF1A1A1A),
                                      image: coverArt != null
                                          ? DecorationImage(image: MemoryImage(coverArt!), fit: BoxFit.cover)
                                          : null,
                                      boxShadow: const [BoxShadow(color: Colors.black87, blurRadius: 50, offset: Offset(0, 25))],
                                      border: Border.all(color: Colors.white24, width: 2),
                                    ),
                                    child: Stack(
                                      alignment: Alignment.center,
                                      children: [
                                        // Overlay to darken image slightly so grooves are visible
                                        if (coverArt != null)
                                          Container(
                                            decoration: BoxDecoration(
                                              shape: BoxShape.circle,
                                              color: Colors.black.withOpacity(0.2),
                                            ),
                                          ),
                                        // Vinyl grooves on top of the image
                                        for (double w = 310; w > 50; w -= 15)
                                          Container(
                                            width: w,
                                            height: w,
                                            decoration: BoxDecoration(
                                              shape: BoxShape.circle,
                                              border: Border.all(color: Colors.black.withOpacity(0.15), width: 1),
                                            ),
                                          ),
                                        // Shine reflection
                                        Container(
                                          decoration: BoxDecoration(
                                            shape: BoxShape.circle,
                                            gradient: LinearGradient(
                                              begin: Alignment.topLeft,
                                              end: Alignment.bottomRight,
                                              colors: [
                                                Colors.white.withOpacity(0.4),
                                                Colors.transparent,
                                                Colors.transparent,
                                                Colors.white.withOpacity(0.1),
                                              ],
                                              stops: const [0.0, 0.3, 0.7, 1.0],
                                            ),
                                          ),
                                        ),
                                        // Spindle hole
                                        Container(
                                          width: 16,
                                          height: 16,
                                          decoration: BoxDecoration(
                                            shape: BoxShape.circle,
                                            color: Colors.black,
                                            border: Border.all(color: Colors.white54, width: 1),
                                            boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 4, offset: Offset(0, 2))],
                                          ),
                                        ),
                                        if (coverArt == null)
                                          const Icon(Icons.music_note, size: 80, color: Colors.white24),
                                      ],
                                    ),
                                  ),
                                ),
                        ),
                        
                        const SizedBox(height: 60),
                        
                        // Text Info
                        Align(
                          alignment: Alignment.centerLeft,
                          child: Text(
                            title,
                            style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.white),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Align(
                          alignment: Alignment.centerLeft,
                          child: Text(
                            artist,
                            style: TextStyle(fontSize: 18, color: Colors.white.withOpacity(0.7)),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                        
                        const SizedBox(height: 16),
                        
                        // Visualizer
                        Align(
                          alignment: Alignment.centerLeft,
                          child: AudioVisualizer(isPlaying: isPlaying, type: visualizerType),
                        ),
                        
                        const SizedBox(height: 24),
                        
                        // Progress Bar
                        SliderTheme(
                          data: SliderThemeData(
                            trackHeight: 4,
                            thumbShape: const RoundSliderThumbShape(enabledThumbRadius: 6),
                            overlayShape: const RoundSliderOverlayShape(overlayRadius: 14),
                            activeTrackColor: Colors.white,
                            inactiveTrackColor: Colors.white.withOpacity(0.2),
                            thumbColor: Colors.white,
                            overlayColor: Colors.white.withOpacity(0.1),
                          ),
                          child: Slider(
                            value: position.inMilliseconds.toDouble(),
                            max: math.max(duration.inMilliseconds.toDouble(), position.inMilliseconds.toDouble() + 1),
                            onChanged: (val) {
                              player.seek(Duration(milliseconds: val.toInt()));
                            },
                          ),
                        ),
                        
                        // Time labels
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 4.0),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(_formatDuration(position), style: TextStyle(color: Colors.white.withOpacity(0.6), fontSize: 12)),
                              Text(_formatDuration(duration), style: TextStyle(color: Colors.white.withOpacity(0.6), fontSize: 12)),
                            ],
                          ),
                        ),
                        
                        const SizedBox(height: 32),
                        
                        // Controls
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                          children: [
                            IconButton(
                              icon: Icon(Icons.shuffle, color: isShuffle ? Colors.blueAccent : Colors.white.withOpacity(0.5)),
                              iconSize: 28,
                              onPressed: () => setState(() => isShuffle = !isShuffle),
                            ),
                            IconButton(
                              icon: const Icon(Icons.skip_previous_rounded, color: Colors.white),
                              iconSize: 48,
                              onPressed: _prev,
                            ),
                            Container(
                              width: 80,
                              height: 80,
                              decoration: const BoxDecoration(shape: BoxShape.circle, color: Colors.white),
                              child: IconButton(
                                icon: Icon(isPlaying ? Icons.pause_rounded : Icons.play_arrow_rounded, color: Colors.black),
                                iconSize: 48,
                                onPressed: () {
                                  if (isPlaying) {
                                    player.pause();
                                  } else {
                                    player.play();
                                  }
                                },
                              ),
                            ),
                            IconButton(
                              icon: const Icon(Icons.skip_next_rounded, color: Colors.white),
                              iconSize: 48,
                              onPressed: _next,
                            ),
                            IconButton(
                              icon: Icon(
                                repeatMode == 0 ? Icons.repeat : (repeatMode == 1 ? Icons.repeat : Icons.repeat_one),
                                color: repeatMode != 0 ? Colors.blueAccent : Colors.white.withOpacity(0.5)
                              ),
                              iconSize: 28,
                              onPressed: () {
                                setState(() {
                                  repeatMode = (repeatMode + 1) % 3;
                                });
                              },
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),'''

new_expanded = '''                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 32.0),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        // Artwork / Vinyl
                        Expanded(
                          child: Center(
                            child: Hero(
                              tag: 'artwork',
                              child: isPodcast
                                  ? AspectRatio(
                                      aspectRatio: 1,
                                      child: Container(
                                        constraints: const BoxConstraints(maxWidth: 350, maxHeight: 350),
                                        decoration: BoxDecoration(
                                          color: Colors.grey[800],
                                          borderRadius: BorderRadius.circular(24),
                                          boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 30, offset: Offset(0, 15))],
                                        ),
                                        child: Padding(
                                          padding: const EdgeInsets.all(48.0),
                                          child: Image.asset('assets/images/podcast_icon.png', color: Colors.blueAccent),
                                        ),
                                      ),
                                    )
                                  : AnimatedBuilder(
                                      animation: _spinController,
                                      builder: (_, child) {
                                        return Transform.rotate(
                                          angle: _spinController.value * 2 * math.pi,
                                          child: child,
                                        );
                                      },
                                      child: AspectRatio(
                                        aspectRatio: 1,
                                        child: Container(
                                          constraints: const BoxConstraints(maxWidth: 380, maxHeight: 380),
                                          decoration: BoxDecoration(
                                            shape: BoxShape.circle,
                                            color: const Color(0xFF1A1A1A),
                                            image: coverArt != null
                                                ? DecorationImage(image: MemoryImage(coverArt!), fit: BoxFit.cover)
                                                : const DecorationImage(image: AssetImage('assets/images/music_icon.png'), fit: BoxFit.cover),
                                            boxShadow: const [BoxShadow(color: Colors.black87, blurRadius: 50, offset: Offset(0, 25))],
                                            border: Border.all(color: Colors.white24, width: 2),
                                          ),
                                          child: Stack(
                                            alignment: Alignment.center,
                                            children: [
                                              if (coverArt != null)
                                                Container(
                                                  decoration: BoxDecoration(
                                                    shape: BoxShape.circle,
                                                    color: Colors.black.withOpacity(0.2),
                                                  ),
                                                ),
                                              for (double w = 350; w > 50; w -= 18)
                                                Container(
                                                  width: w,
                                                  height: w,
                                                  decoration: BoxDecoration(
                                                    shape: BoxShape.circle,
                                                    border: Border.all(color: Colors.black.withOpacity(0.12), width: 1),
                                                  ),
                                                ),
                                              Container(
                                                decoration: BoxDecoration(
                                                  shape: BoxShape.circle,
                                                  gradient: LinearGradient(
                                                    begin: Alignment.topLeft,
                                                    end: Alignment.bottomRight,
                                                    colors: [
                                                      Colors.white.withOpacity(0.4),
                                                      Colors.transparent,
                                                      Colors.transparent,
                                                      Colors.white.withOpacity(0.1),
                                                    ],
                                                    stops: const [0.0, 0.3, 0.7, 1.0],
                                                  ),
                                                ),
                                              ),
                                              Container(
                                                width: 16,
                                                height: 16,
                                                decoration: BoxDecoration(
                                                  shape: BoxShape.circle,
                                                  color: Colors.black,
                                                  border: Border.all(color: Colors.white54, width: 1),
                                                  boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 4, offset: Offset(0, 2))],
                                                ),
                                              ),
                                            ],
                                          ),
                                        ),
                                      ),
                                    ),
                            ),
                          ),
                        ),
                        
                        const SizedBox(height: 20),
                        
                        // Text Info
                        Align(
                          alignment: Alignment.centerLeft,
                          child: Text(
                            title,
                            style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                        const SizedBox(height: 6),
                        Row(
                          children: [
                            Expanded(
                              child: Text(
                                artist,
                                style: TextStyle(fontSize: 16, color: Colors.white.withOpacity(0.7)),
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                            AudioVisualizer(isPlaying: isPlaying, type: visualizerType),
                          ],
                        ),
                        
                        const SizedBox(height: 20),
                        
                        // Progress Bar
                        SliderTheme(
                          data: SliderThemeData(
                            trackHeight: 4,
                            thumbShape: const RoundSliderThumbShape(enabledThumbRadius: 6),
                            overlayShape: const RoundSliderOverlayShape(overlayRadius: 14),
                            activeTrackColor: Colors.white,
                            inactiveTrackColor: Colors.white.withOpacity(0.2),
                            thumbColor: Colors.white,
                            overlayColor: Colors.white.withOpacity(0.1),
                          ),
                          child: Slider(
                            value: position.inMilliseconds.toDouble(),
                            max: math.max(duration.inMilliseconds.toDouble(), position.inMilliseconds.toDouble() + 1),
                            onChanged: (val) {
                              player.seek(Duration(milliseconds: val.toInt()));
                            },
                          ),
                        ),
                        
                        // Time labels
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 4.0),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(_formatDuration(position), style: TextStyle(color: Colors.white.withOpacity(0.6), fontSize: 12)),
                              Text(_formatDuration(duration), style: TextStyle(color: Colors.white.withOpacity(0.6), fontSize: 12)),
                            ],
                          ),
                        ),
                        
                        const SizedBox(height: 16),
                        
                        // Controls
                        Padding(
                          padding: const EdgeInsets.only(bottom: 24.0),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                            children: [
                              IconButton(
                                icon: Icon(Icons.shuffle, color: isShuffle ? Colors.blueAccent : Colors.white.withOpacity(0.5)),
                                iconSize: 28,
                                onPressed: () => setState(() => isShuffle = !isShuffle),
                              ),
                              IconButton(
                                icon: const Icon(Icons.skip_previous_rounded, color: Colors.white),
                                iconSize: 48,
                                onPressed: _prev,
                              ),
                              Container(
                                width: 72,
                                height: 72,
                                decoration: const BoxDecoration(shape: BoxShape.circle, color: Colors.white),
                                child: IconButton(
                                  icon: Icon(isPlaying ? Icons.pause_rounded : Icons.play_arrow_rounded, color: Colors.black),
                                  iconSize: 42,
                                  onPressed: () {
                                    if (isPlaying) {
                                      player.pause();
                                    } else {
                                      player.play();
                                    }
                                  },
                                ),
                              ),
                              IconButton(
                                icon: const Icon(Icons.skip_next_rounded, color: Colors.white),
                                iconSize: 48,
                                onPressed: _next,
                              ),
                              IconButton(
                                icon: Icon(
                                  repeatMode == 0 ? Icons.repeat : (repeatMode == 1 ? Icons.repeat : Icons.repeat_one),
                                  color: repeatMode != 0 ? Colors.blueAccent : Colors.white.withOpacity(0.5)
                                ),
                                iconSize: 28,
                                onPressed: () {
                                  setState(() {
                                    repeatMode = (repeatMode + 1) % 3;
                                  });
                                },
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ),'''

if old_expanded in content:
    content = content.replace(old_expanded, new_expanded)
    open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
    print("UI fixed successfully")
else:
    print("Match failed. Using regex search")
    # Backup regex search for the main structure if whitespace is off
    pass

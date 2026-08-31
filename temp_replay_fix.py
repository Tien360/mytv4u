for file in ["lib/screens/movie_detail_screen.dart", "lib/screens/movie_detail_screen_test.dart"]:
    with open(file, "r", encoding="utf-8") as f:
        c = f.read()

    # 1. Update _playTrailer to seek to 0
    old_play = "await _webviewController.executeScript(\"if(typeof player !== 'undefined' && player && player.playVideo) { player.playVideo(); }\");"
    new_play = "await _webviewController.executeScript(\"if(typeof player !== 'undefined' && player && player.playVideo) { player.seekTo(0); player.playVideo(); }\");"
    c = c.replace(old_play, new_play, 1) # Only for play, not resume!
    
    # 2. Change replay button to call _playTrailer instead of _startInlineTrailer
    old_btn = """                                  onPressed: _trailerEnded
                                      ? _startInlineTrailer
                                      : (_isTrailerPaused
                                          ? _resumeTrailer
                                          : _playTrailer),"""
    new_btn = """                                  onPressed: _trailerEnded
                                      ? _playTrailer
                                      : (_isTrailerPaused
                                          ? _resumeTrailer
                                          : _playTrailer),"""
    c = c.replace(old_btn, new_btn)

    with open(file, "w", encoding="utf-8") as f:
        f.write(c)

print("Fixed replay logic!")

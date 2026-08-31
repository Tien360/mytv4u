with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# 1. REMOVE THE BANNER IMAGE (Keep only the trailer)
banner_start = c.find("1. Background Media")
if banner_start != -1:
    stack_start = c.find("child: Stack(", banner_start)
    stack_end = c.find("              ),", stack_start) # end of Stack
    
    if stack_start != -1 and stack_end != -1:
        new_stack = """child: Stack(
              children: [
                Positioned.fill(
                  child: _showInlineTrailer && _isWebviewInitialized
                      ? Webview(_webviewController)
                      : const SizedBox.shrink(),
                ),
              ],
            )"""
        # wait, the original ends with `),`
        # let's just replace the Positioned.fill block
        pos_start = c.find("Positioned.fill(", stack_start)
        pos_end = c.find("                ),", pos_start)
        if pos_start != -1 and pos_end != -1:
             new_pos = """Positioned.fill(
                  child: _showInlineTrailer && _isWebviewInitialized
                      ? Webview(_webviewController)
                      : const SizedBox.shrink(),
                )"""
             c = c[:pos_start] + new_pos + c[pos_end+18:]

# 2. REMOVE THE Stack and BackdropFilter from the Content SliverToBoxAdapter
# The SliverToBoxAdapter has `child: Stack(` and inside has `Padding(padding: const EdgeInsets.fromLTRB(40, 20, 40, 40),`
padding_idx = c.find("Padding(padding: const EdgeInsets.fromLTRB(40, 20, 40, 40),")
if padding_idx != -1:
    # Find the SliverToBoxAdapter that encloses this Padding
    sliver_idx = c.rfind("SliverToBoxAdapter(", 0, padding_idx)
    if sliver_idx != -1:
        # Get the balanced string of this Padding
        def get_balanced(text, start):
            count = 0
            for i in range(start, len(text)):
                if text[i] == '(': count += 1
                elif text[i] == ')':
                    count -= 1
                    if count == 0: return i
            return -1
            
        padding_end = get_balanced(c, padding_idx + 7) # index of '(' in 'Padding('
        padding_block = c[padding_idx:padding_end+1]
        
        # Now find the end of the SliverToBoxAdapter
        sliver_end = get_balanced(c, sliver_idx + 18)
        
        new_sliver = "SliverToBoxAdapter(\nchild: " + padding_block + "\n)"
        
        c = c[:sliver_idx] + new_sliver + c[sliver_end+1:]

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Removed old banner image and content gradient")

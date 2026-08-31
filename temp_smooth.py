import sys

with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# We need to find `slivers: [`
slivers_idx = c.find("slivers: [")
if slivers_idx != -1:
    # There are two SliverToBoxAdapters. The first is for the empty space (Video).
    # The second is for the Content.
    first_sliver_idx = c.find("SliverToBoxAdapter", slivers_idx)
    second_sliver_idx = c.find("SliverToBoxAdapter", first_sliver_idx + 10)
    
    if second_sliver_idx != -1:
        # We found the second SliverToBoxAdapter.
        # Now we need to find `child: ClipRRect(` or `child: Container(` which is inside it.
        child_idx = c.find("child:", second_sliver_idx)
        
        padding_idx = c.find("child: Padding(", child_idx)
        
        if padding_idx != -1:
            # We will rewrite from second_sliver_idx up to padding_idx
            prefix = """SliverToBoxAdapter(
                        child: Stack(
                          children: [
                            Positioned.fill(
                              child: ShaderMask(
                                shaderCallback: (Rect bounds) {
                                  return const LinearGradient(
                                    begin: Alignment.topCenter,
                                    end: Alignment.bottomCenter,
                                    colors: [Colors.transparent, Colors.white, Colors.white],
                                    stops: [0.0, 0.1, 1.0],
                                  ).createShader(bounds);
                                },
                                blendMode: BlendMode.dstIn,
                                child: BackdropFilter(
                                  filter: ImageFilter.blur(sigmaX: 20.0, sigmaY: 20.0),
                                  child: Container(
                                    decoration: BoxDecoration(
                                      gradient: LinearGradient(
                                        colors: [
                                          Colors.black.withOpacity(0.0),
                                          Colors.black.withOpacity(0.75),
                                          Colors.black.withOpacity(0.95),
                                        ],
                                        begin: Alignment.topCenter,
                                        end: Alignment.bottomCenter,
                                        stops: const [0.0, 0.1, 1.0],
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                            ),
                            """
            
            # Now we need to extract the exact text of `child: Padding( ... )`
            # and replace the closing brackets of the old SliverToBoxAdapter.
            # To do this safely, let's extract the full block of `SliverToBoxAdapter`
            
            def get_balanced(text, start):
                count = 0
                for i in range(start, len(text)):
                    if text[i] == '(': count += 1
                    elif text[i] == ')':
                        count -= 1
                        if count == 0: return i
                return -1
                
            sliver_end = get_balanced(c, second_sliver_idx + len("SliverToBoxAdapter") - 1)
            
            padding_start = padding_idx + len("child: ")
            padding_end = get_balanced(c, padding_start + len("Padding") - 1)
            
            padding_block = c[padding_start:padding_end+1]
            
            new_block = prefix + padding_block + """
                          ],
                        ),
                      )"""
            
            c = c[:second_sliver_idx] + new_block + c[sliver_end+1:]
            
            with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
                f.write(c)
            print("Successfully patched smooth blur transition!")
        else:
            print("Padding not found")
    else:
        print("Second sliver not found")
else:
    print("Slivers not found")

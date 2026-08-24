import re

with open("lib/widgets/ambient_background.dart", "r", encoding="utf-8") as f:
    text = f.read()

text = "import 'dart:convert';\nimport '../utils/noise_asset.dart';\n" + text

old_stack = """                          child: Stack(
                            fit: StackFit.expand,
                            children: [
                              CachedNetworkImage(
                                imageUrl: imageUrl,
                                fit: BoxFit.cover,
                                errorWidget: (context, url, error) => Container(color: const Color(0xFF0F172A)),
                              ),
                              BackdropFilter(
                                filter: ImageFilter.blur(sigmaX: 150.0, sigmaY: 150.0),
                                child: Container(
                                  color: Colors.black.withOpacity(0.6), // Darken the bright colors slightly
                                ),
                              ),
                            ],
                          ),"""

new_stack = """                          child: Stack(
                            fit: StackFit.expand,
                            children: [
                              CachedNetworkImage(
                                imageUrl: imageUrl,
                                fit: BoxFit.cover,
                                errorWidget: (context, url, error) => Container(color: const Color(0xFF0F172A)),
                              ),
                              BackdropFilter(
                                filter: ImageFilter.blur(sigmaX: 150.0, sigmaY: 150.0),
                                child: Container(
                                  color: Colors.black.withOpacity(0.6), // Darken the bright colors slightly
                                ),
                              ),
                              // Noise overlay to prevent color banding
                              Opacity(
                                opacity: 0.04,
                                child: Image.memory(
                                  base64Decode(noiseBase64),
                                  repeat: ImageRepeat.repeat,
                                  fit: BoxFit.none,
                                ),
                              ),
                            ],
                          ),"""

if old_stack in text:
    text = text.replace(old_stack, new_stack)
    with open("lib/widgets/ambient_background.dart", "w", encoding="utf-8") as f:
        f.write(text)
    print("Modified ambient_background.dart")
else:
    print("Could not find stack in ambient_background.dart")

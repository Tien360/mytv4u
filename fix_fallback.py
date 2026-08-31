def fix_fallback_await(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # _tryFallbackDomain is synchronous, cannot use await
    target = "await player.open(Media(newUrl));\n          return true;"
    replacement = "player.open(Media(newUrl));\n          return true;"
    content = content.replace(target, replacement)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_fallback_await('lib/screens/player_screen.dart')
print("Fixed await in synchronous function")

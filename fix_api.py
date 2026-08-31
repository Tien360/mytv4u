content = open('lib/api/sport_api.dart', 'r', encoding='utf-8').read()
content = content.replace("'Giải đấu khác'", "L10n.t(''other-leagues'') ?? 'Giải đấu khác'")
open('lib/api/sport_api.dart', 'w', encoding='utf-8').write(content)

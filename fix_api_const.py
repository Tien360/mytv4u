import re

content = open('lib/api/sport_api.dart', 'r', encoding='utf-8').read()

if 'l10n.dart' not in content:
    content = content.replace("import 'package:http/http.dart' as http;", "import 'package:http/http.dart' as http;\nimport '../utils/l10n.dart';")

content = content.replace("L10n.t(''other-leagues'')", "L10n.t('other-leagues')")

open('lib/api/sport_api.dart', 'w', encoding='utf-8').write(content)

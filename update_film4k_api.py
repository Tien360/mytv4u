import re

with open("lib/api/film4knet_api.dart", "r", encoding="utf-8") as f:
    content = f.read()

if "Film4kProxy.processUrl" not in content:
    content = content.replace("import '../models/movie.dart';", "import '../models/movie.dart';\nimport 'film4k_proxy.dart';")
    content = content.replace("buildFullUrl(movieData['hlsUrl'])", "Film4kProxy.processUrl(buildFullUrl(movieData['hlsUrl']))")
    content = content.replace("buildFullUrl(url)", "Film4kProxy.processUrl(buildFullUrl(url))")
    with open("lib/api/film4knet_api.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("Modified film4knet_api.dart")
else:
    print("Already modified")

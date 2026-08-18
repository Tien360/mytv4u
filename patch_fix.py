import re

with open('lib/api/phim_api.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('''                } else {
                  serversMap[9] = [
                    if (vidsrcServer != null) vidsrcServer,
                    vidApiServer
                  ];''', '''                } else {
                  serversMap[9] = [
                    if (vidsrcServer != null) vidsrcServer,
                    if (vidApiServer != null) vidApiServer
                  ];''')

with open('lib/api/phim_api.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed list nullability')

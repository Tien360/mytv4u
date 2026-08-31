import os
import glob
files = glob.glob(r'T:\flutter\.pub-cache\hosted\*\audiotags-*\lib\src\tag.dart')
if files:
    with open(files[0], 'r', encoding='utf-8') as f:
        content = f.read()
    print([line for line in content.split('\n') if 'String?' in line])
else:
    print('Not found')

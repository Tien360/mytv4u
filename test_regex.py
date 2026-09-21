import re

rawLabel = "1080P.VIE.AI.AMZN.WEB-DL.DDP5.1.H.264.MKV (7.35 GB)"
resMatch = re.search(r'(1080p|2160p|720p|4k)', rawLabel, re.IGNORECASE)
resolution = resMatch.group(1).upper() if resMatch else ""
sizeMatch = re.search(r'([\d\.]+\s*(GB|MB))', rawLabel, re.IGNORECASE)
size = sizeMatch.group(1) if sizeMatch else ""
epName = " - ".join([x for x in [resolution, size] if x])
print(epName)

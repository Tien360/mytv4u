with open('noise_b64.txt', 'r') as f:
    b64 = f.read()

dart_code = f"""
const String noiseBase64 = '{b64}';
"""
with open('lib/utils/noise_asset.dart', 'w', encoding='utf-8') as f:
    f.write(dart_code)
print("Created noise_asset.dart")

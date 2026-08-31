import json
import base64

def normalize_clearkey(kodi_key_str):
    if not kodi_key_str: return {}
    # Format 2: JSON
    if kodi_key_str.startswith("{"):
        try:
            data = json.loads(kodi_key_str)
            keys = {}
            for key_info in data.get("keys", []):
                kid_b64 = key_info.get("kid", "")
                k_b64 = key_info.get("k", "")
                # base64url to hex
                kid_hex = base64.urlsafe_b64decode(kid_b64 + "==").hex()
                k_hex = base64.urlsafe_b64decode(k_b64 + "==").hex()
                keys[kid_hex] = k_hex
            return keys
        except Exception as e:
            print("Failed to parse JSON", e)
            return {}
    # Format 1: hex:hex
    else:
        parts = kodi_key_str.split(":")
        if len(parts) == 2:
            return {parts[0]: parts[1]}
        return {}

print("HBO:", normalize_clearkey('{"keys":[{"kty":"oct","k":"PeDzjc8BSCff1b7Dh0PGog","kid":"Cd3+PWOGPK+ut50FRrCYqw"}],"type":"temporary"}'))
print("VTVPrime 1:", normalize_clearkey("f3d73b3a9b89462ebf7911004ea3b384:682121760c4061b4bd734cfdb3fc697d"))

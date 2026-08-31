import json

paths = ['assets/langs/vi.json', 'assets/langs/en.json']
for path in paths:
    with open(path, 'r', encoding='utf-8') as f:
        d = json.load(f)
    
    # Map the old pending keys to the new unavailable keys
    if 'ep_msg_today_pending' in d:
        d['ep_msg_today_unavailable'] = d['ep_msg_today_pending']
    if 'ep_msg_today_pending_finale' in d:
        d['ep_msg_today_finale_unavailable'] = d['ep_msg_today_pending_finale']
    if 'ep_msg_today_available_finale' in d:
        d['ep_msg_today_finale_available'] = d['ep_msg_today_available_finale']
        
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
print("Updated JSON files")

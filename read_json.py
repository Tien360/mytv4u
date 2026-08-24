import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('livescore.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("last_update:", data.get('last_update'))
print("number of leagues:", len(data.get('leagues', [])))

for i, league in enumerate(data.get('leagues', [])[:2]):
    print(f"\nLeague {i+1}:", league.get('league_name'))
    days = league.get('days', [])
    for d in days[:1]:
        print("  Date:", d.get('date'))
        matches = d.get('matches', [])
        for m in matches[:2]:
            print(f"    {m.get('time')} {m.get('team_home')} {m.get('score')} {m.get('team_away')} [{m.get('status')}]")

"""把 Wowhead 說明框的掉落機率（data/loot/drop_rates.json）放進網站，只當參考（可重複執行）。"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DR = json.load(open(os.path.join(ROOT, 'data/loot/drop_rates.json')))
for p in ['index.html', 'claude-artifact/index.html']:
    path = os.path.join(ROOT, p); s = open(path, encoding='utf-8').read()
    R = json.loads(re.search(r'const RAW_LOOT = (\{.*?\});\n', s).group(1))
    ids = {str(r[0]) for v in R.values() for r in v}
    D = {k: v for k, v in DR.items() if k in ids}
    blob = '/*DROP-BEGIN*/const DROP = ' + json.dumps(D, separators=(',', ':')) + ';/*DROP-END*/\n'
    if '/*DROP-BEGIN*/' in s: s = re.sub(r'/\*DROP-BEGIN\*/.*?/\*DROP-END\*/\n', lambda m: blob, s, flags=re.S)
    else: s = s.replace('function lootFor(id){', blob + 'function lootFor(id){', 1)
    old = '(groups[key] = groups[key] || []).push({id:iid, n, q,'
    if old in s: s = s.replace(old, '(groups[key] = groups[key] || []).push({id:iid, n, q, drop: DROP[iid] != null ? (DROP[iid] < 1 ? "<1" : DROP[iid]) + "%" : undefined,', 1)
    s = s.replace('li.textContent = "完整屬性和掉落機率待補";', 'li.textContent = it.drop ? "完整屬性待補" : "完整屬性和掉落機率待補";')
    open(path, 'w', encoding='utf-8').write(s); print(p, 'drop rates', len(D))

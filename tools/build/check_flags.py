"""比對網站任務的陣營／職業／種族限制和 Wowhead 區域任務清單（data/quests/zone_flags.json）。只列出差異，不修改。"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
m = json.load(open(os.path.join(ROOT, 'data/quests/zone_flags.json')))
CLS = {1:'戰士',2:'聖騎士',4:'獵人',8:'盜賊',16:'牧師',64:'薩滿',128:'法師',256:'術士',1024:'德魯伊'}
RACE = {1:'人類',2:'獸人',4:'矮人',8:'夜精靈',16:'不死族',32:'牛頭人',64:'地精',128:'食人妖'}
h = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
for l in [l for l in h.split('\n') if l.startswith('  {d:')]:
    i = re.search(r',id:(\d+)', l).group(1); n = re.search(r'[{,]n:"([^"]+)"', l).group(1)
    if i not in m: print(i, n, '沒有 Wowhead 區域資料'); continue
    s, rc, rr = m[i]; side = (re.search(r'side:"(\w)"', l) or [0, 'H'])[1]
    ws = {1: 'A', 2: 'H', 3: 'B', 0: 'B'}[s]
    if ws != side: print(i, n, '陣營', side, '→ Wowhead', ws)
    cls = re.search(r'cls:\[([^\]]*)\]', l); race = re.search(r'race:\[([^\]]*)\]', l)
    wc = {v for k, v in CLS.items() if rc & k}; sc = set(re.findall(r'"([^"]+)"', cls.group(1))) if cls else set()
    if wc != sc: print(i, n, '職業', sorted(sc), '→ Wowhead', sorted(wc))
    wr = {v for k, v in RACE.items() if rr & k}; sr = set(re.findall(r'"([^"]+)"', race.group(1))) if race else set()
    if wr != sr: print(i, n, '種族', sorted(sr), '→ Wowhead', sorted(wr))

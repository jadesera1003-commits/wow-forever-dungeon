"""把「系列進度」注入網站：本任務在系列第幾步、後面哪一步給獎勵、要不要再進副本。

資料來源：
  data/quests/series_*.json   {qid:[系列任務ID[], 交任務NPC[id,名]|null, [區域,[x,y]|null]|null, 固定獎勵[], 擇一獎勵[], 目標]}
  data/quests/details*.json   系列名稱（和 ID 同順序）
  data/quests/deep_*.json     本步獎勵
  data/items/reward_items.json
以 /*QS-BEGIN*/ … /*QS-END*/ 標記，可重複執行。
"""
import json, glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = lambda *a: os.path.join(ROOT, *a)
load = lambda f: json.load(open(f, encoding='utf-8'))

SER = {}
for f in sorted(glob.glob(P('data/quests/series_*.json'))): SER.update(load(f))
DET = {}
for f in glob.glob(P('data/quests/details*.json')):
    d = load(f)
    if isinstance(d, dict): DET.update(d)
DEEP = {}
for f in glob.glob(P('data/quests/deep_[0-9]*.json')) + glob.glob(P('data/quests/deep_heads*.json')): DEEP.update(load(f))
ITEMS = load(P('data/items/reward_items.json'))

INST = ['黑澗深淵', '奧達曼', '剃刀高地', '剃刀沼澤', '黑石深淵', '黑石塔', '斯坦索姆', '通靈學院', '厄運之槌',
        '血色修道院', '奧卡茲監獄', '挖掘場', '克羅多克要塞', '沉沒的神廟', '阿塔哈卡神廟', '瑪拉頓', '諾姆瑞根',
        '死亡礦坑', '影牙城堡', '祖爾法拉克', '哀嚎洞穴', '怒焰裂谷', '監獄', '黑喉要塞', '沉沒之城', '羅德隆廢墟',
        '暮光之罩', '族長之廳', '達拉然城']

def det_names(qid):
    v = DET.get(qid)
    if v is None: return None
    if isinstance(v, dict): return v['series']
    return v[9] if len(v) == 13 else v[8]

def title(qid):
    s = SER.get(qid) or DEEP.get(qid)
    t = (s[5] if qid in SER else s[4]) if s else ''
    return t.split(' ')[0] if t else ''

def in_inst(qid):
    s = SER.get(qid)
    if not s: return None
    z = s[2]
    if z and (z[0] in INST or z[1] == [0, 0]): return True
    obj = s[5].split(' ', 1)[-1]
    return any(n in obj for n in INST)

def rewards(qid):
    if qid in SER: return SER[qid][3], SER[qid][4]
    if qid in DEEP: return DEEP[qid][2], DEEP[qid][3]
    return [], []

def build(site):
    QS, used = {}, set()
    for qid in site:
        s = SER.get(qid)
        if not s: continue
        ids = [str(x) for x in s[0]]
        if qid not in ids: continue
        # Wowhead 的系列表有時漏掉最後的「交任務」步驟：用前置關係往後接
        while True:
            nxt = [k for k, v in DEEP.items() if ids[-1] in map(str, v[0]) and k not in ids]
            if len(nxt) != 1: break
            ids.append(nxt[0])
        if len(ids) < 2 or ids[-1] == qid: continue
        names = det_names(qid)
        if not (isinstance(names, list) and len(names) == len(ids)): names = None
        p = ids.index(qid)
        steps = []
        for i, x in enumerate(ids):
            n = title(x) or (names[i] if names else '') or ('任務 #' + x)
            g, c = rewards(x)
            steps.append([int(x), n, 1 if (g or c) else 0])
        later = []
        cz = s[2]
        left = in_inst(qid) is False or bool(cz and cz[0] not in INST and cz[1] not in (None, [0, 0]))
        again = []
        for i in range(p + 1, len(ids)):
            x = ids[i]; sx = SER.get(x)
            ii = in_inst(x)
            if ii and left: again.append(i); left = False
            if ii is False: left = True
            elif ii and sx and sx[2] and sx[2][0] not in INST and sx[2][1] not in (None, [0, 0]): left = True
            g, c = rewards(x)
            if g or c:
                npc = sx[1][1] if sx and sx[1] else ''
                w = ''
                if sx and sx[2]:
                    z, co = sx[2]
                    w = z + (' (%s, %s)' % (co[0], co[1]) if co and co != [0, 0] else '')
                later.append([i, npc, w, g, c]); used |= set(map(str, g + c))
        out_only = all(in_inst(ids[i]) is False for i in range(p + 1, len(ids)))
        QS[qid] = {'p': p, 's': steps, 'r': later, 'a': again, 'o': 1 if out_only else 0}
    return QS, used

for path in [P('index.html'), P('claude-artifact', 'index.html')]:
    h = open(path, encoding='utf-8').read()
    site = set(re.findall(r',id:(\d+)', h))
    QS, used = build(site)
    m = re.search(r'const RIT = (\{.*?\});\n', h)
    rit = json.loads(m.group(1)) if m else {}
    for k in used:
        if k in ITEMS: rit[k] = ITEMS[k]
    h = h.replace(m.group(0), 'const RIT = ' + json.dumps(rit, ensure_ascii=False, separators=(',', ':')) + ';\n') if m else h
    blob = '/*QS-BEGIN*/\nconst QS = ' + json.dumps(QS, ensure_ascii=False, separators=(',', ':')) + ';\n/*QS-END*/\n'
    if '/*QS-BEGIN*/' in h:
        h = re.sub(r'/\*QS-BEGIN\*/.*?/\*QS-END\*/\n', lambda _: blob, h, flags=re.S)
    else:
        h = h.replace('/*QX-END*/\n', '/*QX-END*/\n' + blob, 1)
    open(path, 'w', encoding='utf-8').write(h)
    print(os.path.relpath(path, ROOT), 'series', len(QS), 'with later reward', sum(1 for v in QS.values() if v['r']),
          'run again', sum(1 for v in QS.values() if v['a']))

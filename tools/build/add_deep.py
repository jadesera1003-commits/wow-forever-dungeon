"""把深度爬取（獎勵、後續解鎖、任務目標）注入 index.html 與 claude-artifact/index.html。

資料來源：
  data/quests/deep_*.json       {qid:[req[], unl[], 固定獎勵[], 選擇獎勵[], 目標文字]}
  data/items/reward_items.json  {itemId:[名稱, 品質, "部位 類型"]}
重複執行會覆蓋上一次注入的內容（以 /*QX-BEGIN*/ … /*QX-END*/ 標記）。
"""
import json, glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = lambda *a: os.path.join(ROOT, *a)

D = {}
for f in sorted(glob.glob(P('data/quests/deep_[0-9]*.json'))) + sorted(glob.glob(P('data/quests/deep_heads*.json'))):
    D.update(json.load(open(f, encoding='utf-8')))
ITEMS = json.load(open(P('data/items/reward_items.json'), encoding='utf-8'))
DET = {}
for f in glob.glob(P('data/quests/details*.json')):
    d = json.load(open(f, encoding='utf-8'))
    if isinstance(d, dict): DET.update(d)
# Wowhead 標「本任務不可共享」；SHARE_FIX 放玩家實測的修正（True＝可以分享）
SHARE_FIX = {}
def no_share(qid):
    if qid in SHARE_FIX: return not SHARE_FIX[qid]
    v = DET.get(qid)
    if v is None: return None
    return bool(v.get('ns') if isinstance(v, dict) else v[7])

# 後續解鎖的重要程度（人工判斷：依任務內容與 Wowhead 頁面）
#   main = 副本任務（本站有收錄）  imp = 重要系列  gear = 後續有裝備獎勵  end = 收尾／送信對話  next = 一般後續
TAG = {
    '598': 'next', '728': 'end', '727': 'end', '5461': 'imp',
    '8985': 'imp', '8986': 'imp', '8987': 'imp', '8988': 'imp',
    '2279': 'end', '2280': 'gear', '2440': 'gear', '2340': 'gear',
    '2949': 'gear', '2948': 'gear', '3374': 'imp', '3512': 'imp',
    '5068': 'gear', '5063': 'gear', '5067': 'gear',
    '3370': 'gear', '3369': 'gear', '1491': 'next', '2501': 'next', '2965': 'gear',
}
NOTE = {  # 補充說明（只寫有用的）
    '5461': '通靈學院「巫妖萊斯·霜語」系列的下一步，要去阿拉希高地',
    '3374': '綠龍軍團系列，後面還有好幾步',
    '3512': '綠龍軍團系列',
    '8985': '瓦薩拉克護符系列（黑石塔），四選一材料',
    '5068': '要大量材料＋金幣才換得到',
    '5063': '要大量材料＋金幣才換得到',
    '5067': '要大量材料＋金幣才換得到',
}
NOTE['8986'] = NOTE['8987'] = NOTE['8988'] = NOTE['8985']

SER = {}
for f in glob.glob(P('data/quests/series_*.json')): SER.update(json.load(open(f, encoding='utf-8')))
A_KW = ['達納蘇斯', '鐵爐堡', '暴風城', '塞拉摩', '羽月要塞', '尼耶爾前哨站', '米奈希爾港', '冰風營地', '遠境堡']
H_KW = ['奧格瑪', '雷霆崖', '幽暗城', '長者高地', '莫沙徹營地', '卡加斯', '亡靈壁壘', '羅格瑪', '葬影村', '布瑞爾']
def side_of(x):
    t = (D.get(x) or ['', '', '', '', ''])[4] + ' ' + ((SER.get(x) or [0, 0, ['']])[2] or [''])[0]
    a = any(k in t for k in A_KW); h = any(k in t for k in H_KW)
    return 'A' if a and not h else 'H' if h and not a else ''

def title(v):
    return v[4].split(' ')[0] if v and v[4] else ''

def objective(v):
    t = v[4]
    parts = t.split(' ', 1)
    t = parts[1] if len(parts) > 1 else ''
    t = re.sub(r'\s*（\s*\d+\s*）', '', t)
    t = re.sub(r'\s*(已提供物品：.*|（已提供）.*)$', '', t).strip()
    t = t.replace('&lt;', '<').replace('&gt;', '>')
    if '。' in t: t = t[:t.rindex('。') + 1]
    return t[:110]

for path in [P('index.html'), P('claude-artifact', 'index.html')]:
    if not os.path.exists(path):
        continue
    h = open(path, encoding='utf-8').read()
    site = set(re.findall(r',id:(\d+)', h))
    QX, used = {}, set()
    for qid in site:
        v = D.get(qid)
        if not v:
            continue
        e = {}
        o = objective(v)
        if o: e['o'] = o
        give = [x for x in v[2] if x not in v[3]]  # Wowhead 有時把擇一物品也列在「還會收到」，以擇一為準
        if give: e['g'] = give; used |= set(map(str, give))
        if v[3]: e['c'] = v[3]; used |= set(map(str, v[3]))
        if no_share(qid): e['ns'] = 1
        u = []
        for x in v[1]:
            x = str(x)
            tag = 'main' if x in site else TAG.get(x, 'next')
            dx = D.get(x) or ['', '', [], [], '']
            dx = dx[:2] + [[i for i in dx[2] if i not in dx[3]]] + dx[3:]
            used |= set(map(str, dx[2] + dx[3]))
            u.append([int(x), title(D.get(x)) or ('任務 #' + x), tag, NOTE.get(x, ''), side_of(x), dx[2], dx[3]])
        if u: e['u'] = u
        if e: QX[qid] = e
    RIT = {k: ITEMS[k] for k in sorted(used, key=int) if k in ITEMS}
    blob = ('/*QX-BEGIN*/\nconst QX = ' + json.dumps(QX, ensure_ascii=False, separators=(',', ':')) +
            ';\nconst RIT = ' + json.dumps(RIT, ensure_ascii=False, separators=(',', ':')) + ';\n/*QX-END*/\n')
    if '/*QX-BEGIN*/' in h:
        h = re.sub(r'/\*QX-BEGIN\*/.*?/\*QX-END\*/\n', lambda m: blob, h, flags=re.S)
    else:
        h = h.replace('const RAW_LOOT = ', blob + 'const RAW_LOOT = ', 1)
    open(path, 'w', encoding='utf-8').write(h)
    print(os.path.relpath(path, ROOT), 'quests', len(QX), 'items', len(RIT))

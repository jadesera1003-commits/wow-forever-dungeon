import os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json,re,sys
Q=os.path.join(ROOT,'data/quests/')
D={}
for i in range(1,11): D.update(json.load(open(Q+f'details2_{i}.json')))
SIDE={'聯盟':'A','部落':'H','雙方':'B'}
def loc(v): return f"{v[9]} ({v[10][0]:.1f}, {v[10][1]:.1f})"
A=[]
def add(d,i,c,**k):
    v=D[str(i)]; e={'d':d,'c':c,'n':v[0],'lv':v[1]}
    if v[11]: e['xp']=v[11]
    if c in('direct','chain') and v[10] and v[10]!=[0,0]: e['npc']=v[4] or '東瘟疫之地的 NPC'; e['w']=loc(v)
    e.update(k); e['side']=SIDE[v[3]]; e['id']=i; A.append(e)
S='strat'; GH='布德利是鬼魂，要帶「超維度幽靈顯形器」才看得到'
add(S,5212,'direct'); add(S,5214,'direct'); add(S,5243,'direct'); add(S,5251,'direct')
add(S,6163,'direct')
add(S,84318,'direct',npc='東瘟疫之地的 NPC（Wowhead 未標名稱）')
add(S,5122,'inside',npc='奧里克斯',w='副本內'); add(S,5125,'inside',npc='奧里克斯',w='副本內')
add(S,5262,'inside',npc='物品開始',w='副本內掉落',note='交給東瘟疫之地的尼古拉斯·瑟倫霍夫公爵')
add(S,5464,'inside',npc='物件：米奈希爾的禮物',w='副本內',note='交給東瘟疫之地的萊尼德·巴薩羅梅')
add(S,5282,'chain',src={'q':'永不安息的靈魂（第 1 步）','npc':'伊根','w':'東瘟疫之地 (14.4, 33.6)','path':'永不安息的靈魂（第 1 步）→ 永不安息的靈魂'})
add(S,5463,'chain',src={'q':'萊斯·霜語','npc':'馬杜克鎮長','w':'西瘟疫之地 (70.4, 74.0)','path':'萊斯·霜語 → 亡靈萊斯·霜語 → 米奈希爾的禮物'})
add(S,5848,'chain',src={'q':'救贖','npc':'提里奧·弗丁','w':'東瘟疫之地','path':'救贖 → 遺忘的記憶 → 失落的榮耀 → 愛與家庭'})
add(S,8968,'chain',src={'q':'重要的材料','npc':'布德利','w':'黑石山 (32.2, 25.6)','path':'重要的材料 → 瓦薩拉克護符的左半塊'},tip=GH)
add(S,8991,'chain',src={'q':'更多重要的材料','npc':'布德利','w':'黑石山 (32.2, 25.6)','path':'更多重要的材料 → 瓦薩拉克護符的右半塊'},tip=GH)
add(S,5213,'skip',reason='要先交「血肉不會撒謊」才接得到，得再打一趟')
add(S,5263,'skip',reason='要先交「可怕的真相」才接得到，得再打一趟')
add(S,8945,'skip',reason='T0.5 套裝任務鏈，要先做完布德利那幾步')
add(S,8946,'skip',reason='T0.5 套裝任務鏈，接在「逝者的請求」之後')
add(S,8970,'skip',reason='交完左半塊之後的後續')
add(S,84319,'skip',reason='接在「欸！」之後，要先交前一步')
add(S,84330,'skip',reason='接在「不會吧！」之後，要先交前一步')
C='scholo'
add(C,5341,'direct'); add(C,5343,'direct'); add(C,5382,'direct'); add(C,5529,'direct')
add(C,5582,'inside',npc='物品開始',w='副本內掉落',note='交給東瘟疫之地的貝蒂娜·比格辛克')
add(C,4771,'chain',src={'q':'萊尼德·巴薩羅梅','npc':'萊尼德·巴薩羅梅','w':'東瘟疫之地 (81.6, 57.8)','path':'萊尼德·巴薩羅梅 → 貝蒂娜·比格辛克 → 黎明先鋒'})
add(C,5466,'chain',src={'q':'萊斯·霜語','npc':'馬杜克鎮長','w':'西瘟疫之地 (70.4, 74.0)','path':'萊斯·霜語 → … → 米奈希爾的禮物（斯坦索姆）→ 禁錮靈魂的遺物 → 巫妖萊斯·霜語'})
add(C,7647,'chain',cls=['聖騎士'],src={'q':'上古聖馬之魂','npc':'格雷森·沙東布瑞克公爵','w':'暴風城 (48.6, 50.0)','path':'上古聖馬之魂 → 受祝福的奧金馬鎧 → 預言水晶球 → 審判和救贖'})
add(C,5531,'skip',reason='傳話任務，沒有副本目標')
add(C,5515,'skip',reason='要先交「瑟爾林·卡斯迪諾夫教授」才接得到，得再打一趟')
add(C,5384,'skip',reason='接在「卡斯迪諾夫的恐懼之袋」之後，得再打一趟')
def apply(path):
    s=open(path).read()
    if '斯坦索姆・通靈學院 ----' not in s:
        st=s.index('const QUESTS = [');en=s.index('\n];',st)
        lines=['  {'+','.join(f'{k}:{json.dumps(v,ensure_ascii=False)}' for k,v in e.items())+'},' for e in A]
        s=s[:en]+'\n  /* ---- 斯坦索姆・通靈學院 ---- */\n'+'\n'.join(lines)+s[en:]
    m=re.search(r'const PENDING_Q = (\{.*?\});',s,flags=re.S)
    p=json.loads(m.group(1)); p.pop('strat',None); p.pop('scholo',None)
    s=s[:m.start()]+'const PENDING_Q = '+json.dumps(p,ensure_ascii=False,separators=(',',':'))+';'+s[m.end():]
    open(path,'w').write(s)
print(len(A))
for p in sys.argv[1:]: apply(p); print('ok',p)

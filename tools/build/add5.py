import os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json,re,sys
Q=os.path.join(ROOT,'data/quests/')
D={}
for i in range(1,10): D.update(json.load(open(Q+f'details2_{i}.json')))
SIDE={'聯盟':'A','部落':'H','雙方':'B'}
def loc(v): return f"{v[9]} ({v[10][0]:.1f}, {v[10][1]:.1f})"
A=[]
def add(d,i,c,**k):
    v=D[str(i)]; e={'d':d,'c':c,'n':v[0],'lv':v[1]}
    if v[11]: e['xp']=v[11]
    if c in('direct','chain') and v[10] and v[10]!=[0,0]: e['npc']=v[4]; e['w']=loc(v)
    e.update(k); e['side']=SIDE[v[3]]; e['id']=i; A.append(e)
X='dmaul'
IN=lambda n:dict(npc=n,w='副本內')
add(X,7441,'direct'); add(X,7481,'direct'); add(X,7482,'direct')
add(X,7488,'direct',tip='「羽月要塞」只是暴風城的引導任務'); add(X,7489,'direct',tip='「莫沙徹營地」只是幽暗城的引導任務')
add(X,1193,'inside',**IN('物件：損壞的陷阱'),tip='可重複')
add(X,5518,'inside',**IN('諾特·希姆加克')); add(X,5525,'inside',**IN('諾特·希姆加克'))
add(X,5528,'inside',**IN('踐踏者克雷格'),tip='可重複')
add(X,7703,'inside',**IN('克羅卡斯'),note='北區打完國王後接')
add(X,7461,'inside',**IN('辛德拉古靈')); add(X,7877,'inside',**IN('辛德拉古靈'),note='接在「伊莫塔爾的瘋狂」之後')
add(X,7463,'inside',**IN('博學者萊德羅斯'))
for i in (7483,7484,7485): add(X,i,'inside',npc='博學者萊德羅斯',w='副本內・需要聖契物品')
CB={7498:'盜賊',7499:'戰士',7500:'法師',7501:'聖騎士',7502:'術士',7503:'獵人',7504:'牧師',7505:'薩滿',7506:'德魯伊'}
for i,c in CB.items(): add(X,i,'inside',npc='物品：職業書',w='副本內掉落',cls=[c],note='交給副本裡的博學者')
add(X,7507,'inside',npc='物品：諾斯卓的屠龍技術綱要',w='副本內掉落')
add(X,7508,'inside',npc='物品開始',w='副本內掉落')
for i in (7649,7650,7651): add(X,i,'inside',npc='物品開始',w='副本內掉落')
add(X,7643,'direct',cls=['聖騎士'],tip='聖騎士史詩坐騎任務鏈，前面還有好幾步')
add(X,7644,'inside',cls=['聖騎士'],npc='上古聖馬之魂',w='副本內')
add(X,7631,'chain',cls=['術士'],src={'q':'術士史詩坐騎任務鏈','npc':'莫蘇爾·召血者','w':'燃燒平原 (12.6, 31.6)','path':'術士史詩坐騎任務鏈 → 克索諾斯恐懼戰馬'})
GH='布德利是鬼魂，要帶「超維度幽靈顯形器」才看得到'
add(X,8967,'chain',src={'q':'重要的材料','npc':'布德利','w':'黑石山 (32.2, 25.6)','path':'重要的材料 → 瓦薩拉克護符的左半塊'},tip=GH)
add(X,8990,'chain',src={'q':'更多重要的材料','npc':'布德利','w':'黑石山 (32.2, 25.6)','path':'更多重要的材料 → 瓦薩拉克護符的右半塊'},tip=GH)
add(X,7509,'skip',reason='鑄造奎爾塞拉第 2 步要奧妮克希亞的材料')
add(X,8949,'skip',reason='T0.5 套裝任務鏈的後段，要先做完東瘟疫之地的安希恩那幾步')
add(X,8950,'skip',reason='T0.5 套裝任務鏈的後段，接在「法琳的仇恨」之後')
add(X,1318,'skip',reason='同名任務的另一個版本，請看「戈多克巨魔的事務」（克羅卡斯）')
add(X,5519,'skip',reason='可重複版本'); add(X,7429,'skip',reason='可重複版本'); add(X,7462,'skip',reason='同名任務的另一個版本')
add(X,7492,'skip',reason='幽暗城的傳話任務，沒有副本目標'); add(X,7494,'skip',reason='暴風城的傳話任務，沒有副本目標')
def apply(path):
    s=open(path).read()
    if '厄運之槌 ----' not in s:
        st=s.index('const QUESTS = [');en=s.index('\n];',st)
        lines=['  {'+','.join(f'{k}:{json.dumps(v,ensure_ascii=False)}' for k,v in e.items())+'},' for e in A]
        s=s[:en]+'\n  /* ---- 厄運之槌 ---- */\n'+'\n'.join(lines)+s[en:]
    m=re.search(r'const PENDING_Q = (\{.*?\});',s,flags=re.S)
    p=json.loads(m.group(1)); p.pop('dmaul',None)
    s=s[:m.start()]+'const PENDING_Q = '+json.dumps(p,ensure_ascii=False,separators=(',',':'))+';'+s[m.end():]
    open(path,'w').write(s)
print(len(A))
for p in sys.argv[1:]: apply(p); print('ok',p)

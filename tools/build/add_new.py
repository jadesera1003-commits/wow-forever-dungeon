import os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json,re,sys
Q=os.path.join(ROOT,'data/quests/')
Z={}
for f in ['zones_new_1.json','zones_new_2.json','zones_new_3.json']: Z.update(json.load(open(Q+f)))
NEW=[('alcaz','奧卡茲監獄','48–53'),('st','沉沒的神廟','50–60'),('brd','黑石深淵','52–60'),('blackmaw','黑喉要塞','52–60'),('dmaul','厄運之槌','54–60'),('strat','斯坦索姆','55–60'),('scholo','通靈學院','55–60'),('brs','黑石塔','55–60')]
D=json.load(open(Q+'details2_1.json'))
def loc(v): return f"{v[9]} ({v[10][0]:.1f}, {v[10][1]:.1f})"
A=[]
def add(i,c,**k):
    v=D[str(i)]; e={'d':'alcaz','c':c,'n':v[0],'lv':v[1]}
    if v[11]: e['xp']=v[11]
    if c in('direct','chain'): e['npc']=v[4]; e['w']=loc(v)
    e.update(k); e['side']={'聯盟':'A','部落':'H','雙方':'B'}[v[3]]; e['id']=i; A.append(e)
add(96332,'direct',note='塵泥沼澤北邊的部落營地接')
add(96334,'direct',note='交給伊崔格')
add(96376,'direct',tip='不可共享')
add(96377,'direct',tip='不可共享')
add(96379,'direct',tip='兩個陣營都能接，不可共享')
add(96381,'direct')
add(96772,'direct')
add(95263,'inside',npc='副本內接續',w='接在「秘密監獄」之後',note='交給蘇利‧麥拉利')
add(95454,'inside',npc='物品／副本內開始',w='副本內開始',note='之後的「給弗卡爾的壞消息」「索爾必須知道」是出副本後的回報')
add(96335,'inside',en='The Man in the Iron Chains',npc='副本內開始',w='副本內開始')
add(96337,'inside',npc='副本內開始',w='副本內開始',note='交給康納利的大箱')
add(95262,'chain',src={'q':'塞拉摩的眼線','npc':'NPC 待查','w':'塵泥沼澤','path':'塞拉摩的眼線 → 小心背後 → 王者歸來？ → 秘密監獄'})
add(95309,'chain',src={'q':'失蹤的柯爾克隆','npc':'NPC 待查','w':'塵泥沼澤','path':'失蹤的柯爾克隆 → 精英中的精英 → 對的地點，錯的時機 → 不放棄任何一個獸人'})
add(96369,'skip',reason='「柯爾克隆的榮耀」交完後的回報任務，出副本才做')
add(95483,'skip',reason='回奧格瑪找索爾的回報任務，出副本才做')
def apply(path):
    s=open(path).read()
    if 'id:"alcaz"' not in s:
        s=s.replace('  {id:"mara",    name:"瑪拉頓",           lr:"46–55"}\n];','  {id:"mara",    name:"瑪拉頓",           lr:"46–55"},\n'+',\n'.join(f'  {{id:"{i}", name:"{n}", lr:"{l}"}}' for i,n,l in NEW)+'\n];')
    if '奧卡茲監獄 ----' not in s:
        st=s.index('const QUESTS = [');en=s.index('\n];',st)
        lines=['  {'+','.join(f'{k}:{json.dumps(v,ensure_ascii=False)}' for k,v in e.items())+'},' for e in A]
        s=s[:en]+'\n  /* ---- 奧卡茲監獄 ---- */\n'+'\n'.join(lines)+s[en:]
    pend={k:[[q[0],q[1],q[4],q[2],q[3]] for q in Z[k]['qs']] for k in ['st','brd','blackmaw','dmaul','strat','scholo','brs']}
    s=re.sub(r'const PENDING_Q = \{.*?\};','const PENDING_Q = '+json.dumps(pend,ensure_ascii=False,separators=(',',':'))+';',s,count=1,flags=re.S)
    open(path,'w').write(s)
for p in sys.argv[1:]: apply(p); print('ok',p)

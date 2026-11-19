import os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json,re,sys
Q=os.path.join(ROOT,'data/quests/')
D={}
for i in (1,2,3): D.update(json.load(open(Q+f'details2_{i}.json')))
SIDE={'聯盟':'A','部落':'H','雙方':'B'}
def loc(v): return f"{v[9]} ({v[10][0]:.1f}, {v[10][1]:.1f})"
A=[]
def add(d,i,c,**k):
    v=D[str(i)]; e={'d':d,'c':c,'n':v[0],'lv':v[1]}
    if v[11]: e['xp']=v[11]
    if c in('direct','chain') and v[10]: e['npc']=v[4]; e['w']=loc(v)
    e.update(k); e['side']=SIDE[v[3]]; e['id']=i; A.append(e)
B='blackmaw'
add(B,92069,'direct')
add(B,92066,'direct',npc='艾薩拉的 NPC（Wowhead 未標名稱）')
add(B,97327,'direct',npc='艾薩拉的 NPC（Wowhead 未標名稱）')
add(B,97173,'direct'); add(B,97198,'direct')
add(B,92067,'inside',npc='副本內開始',w='副本內開始')
add(B,92070,'inside',en='A Lost Memento',npc='副本內開始',w='副本內開始')
add(B,92065,'chain',src={'q':'Timbermaw Reinforcements','npc':'守門者暴吼','w':'艾薩拉 (42.4, 20.2)','path':'Timbermaw Reinforcements → Chieftain Bloodmaw → 黑喉反擊'})
add(B,92343,'chain',src={'q':'諾達希爾之下','npc':'NPC 待查','w':'待查','path':'諾達希爾之下 → 追根究柢'})
add(B,92344,'chain',src={'q':'諾達希爾之下','npc':'NPC 待查','w':'待查','path':'諾達希爾之下 → 追根究柢'})
add(B,96246,'skip',reason='同名任務的另一個版本，Wowhead 沒有經驗值資料')
S='st'
add(S,1446,'direct'); add(S,3446,'direct',tip='原版要先做「石環」，接不到的話先去做')
add(S,3447,'direct')
add(S,3373,'inside',npc='物品：伊蘭尼庫斯精華',w='副本內掉落')
add(S,8733,'inside',npc='瑪法里恩·怒風',w='副本內開始',tip='60 級任務')
add(S,1445,'chain',src={'q':'淚水之池','npc':'費澤盧爾','w':'悲傷沼澤 (48.0, 55.0)','path':'淚水之池 → 阿塔萊流放者（辛特蘭）→ 向費澤盧爾覆命 → 阿塔哈卡神廟'})
add(S,1475,'chain',n='進入阿塔哈卡神廟',en="Into The Temple of Atal'Hakkar",src={'q':'拉普索迪的故事','npc':'NPC 待查','w':'待查','path':'拉普索迪的故事 → 進入阿塔哈卡神廟'})
add(S,3528,'chain',src={'q':'尖嘯者的靈魂','npc':'葉基亞','w':'塔納利斯 (66.8, 22.4)','path':'尖嘯者的靈魂 → 摩沙魯的預言 → 遠古之卵 → 神靈哈卡'})
add(S,3380,'skip',reason='引導任務，帶你去塔納利斯找瑪爾馮·瑞文斯克，沒有副本目標')
def apply(path):
    s=open(path).read()
    if '黑喉要塞・沉沒的神廟 ----' not in s:
        st=s.index('const QUESTS = [');en=s.index('\n];',st)
        lines=['  {'+','.join(f'{k}:{json.dumps(v,ensure_ascii=False)}' for k,v in e.items())+'},' for e in A]
        s=s[:en]+'\n  /* ---- 黑喉要塞・沉沒的神廟 ---- */\n'+'\n'.join(lines)+s[en:]
    m=re.search(r'const PENDING_Q = (\{.*?\});',s,flags=re.S)
    p=json.loads(m.group(1)); p.pop('blackmaw',None); p.pop('st',None)
    s=s[:m.start()]+'const PENDING_Q = '+json.dumps(p,ensure_ascii=False,separators=(',',':'))+';'+s[m.end():]
    open(path,'w').write(s)
for p in sys.argv[1:]: apply(p); print('ok',p)

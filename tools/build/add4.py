import os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json,re,sys
Q=os.path.join(ROOT,'data/quests/')
D={}
for i in range(1,8): D.update(json.load(open(Q+f'details2_{i}.json')))
SIDE={'聯盟':'A','部落':'H','雙方':'B'}
def loc(v): return f"{v[9]} ({v[10][0]:.1f}, {v[10][1]:.1f})"
A=[]
def add(d,i,c,**k):
    v=D[str(i)]; e={'d':d,'c':c,'n':v[0],'lv':v[1]}
    if v[11]: e['xp']=v[11]
    if c in('direct','chain') and v[10] and v[10]!=[0,0]: e['npc']=v[4]; e['w']=loc(v)
    e.update(k); e['side']=SIDE[v[3]]; e['id']=i; A.append(e)
X='brs'
IN=dict(w='副本內')
# Horde
add(X,4724,'direct'); add(X,4768,'direct',tip='前面的「薇薇安·拉格雷和黑暗石板」只是幽暗城的引導任務')
add(X,4981,'direct',tip='到副本裡找比修')
add(X,4903,'inside',npc='物品：重要的黑石文件',w='副本內掉落',note='交給荒蕪之地・卡加斯的軍官高圖斯')
add(X,4982,'inside',npc='比修',**IN); add(X,4983,'inside',npc='比修',**IN,note='交給卡加斯的雷克斯洛特')
add(X,6569,'chain',src={'q':'風吹來的消息','npc':'NPC 待查','w':'待查','path':'風吹來的消息 → 部落的勇士 → 雷克薩的證明 → 黑龍幻象'})
add(X,6602,'chain',src={'q':'龍骨試煉，埃克托茲','npc':'NPC 待查','w':'待查','path':'龍骨試煉，埃克托茲 → 晉升…… → 黑龍勇士之血'})
add(X,4974,'skip',reason='要先在黑石塔拿到文件開始「高圖斯的命令」，交完才接得到，得再打一趟')
add(X,4769,'skip',reason='幽暗城的傳話任務，沒有副本目標'); add(X,98325,'skip',reason='傳話任務，沒有副本目標')
# Alliance
add(X,4701,'direct'); add(X,4764,'direct',tip='前面的「瑪亞拉·布萊特文」只是暴風城的引導任務')
add(X,5001,'inside',npc='比修',**IN); add(X,5002,'inside',npc='比修',**IN,note='交給燃燒平原的麥克斯韋爾元帥')
add(X,5089,'inside',npc='物品：達基薩斯將軍的命令',w='副本內掉落',note='交給燃燒平原的麥克斯韋爾元帥')
add(X,6502,'chain',src={'q':'潛藏者','npc':'NPC 待查','w':'待查','path':'潛藏者 → 巨龍之眼 → 龍火護符'})
add(X,4765,'skip',reason='交完扣環之後的送貨任務，沒有副本目標'); add(X,4766,'skip',reason='暴風城的傳話任務，沒有副本目標')
add(X,5081,'skip',reason='要先交「給麥斯威爾的訊息」才接得到，得再打一趟')
add(X,5102,'skip',reason='要先交「達基薩斯將軍的命令」才接得到，得再打一趟')
# Both
add(X,4729,'direct'); add(X,4862,'direct'); add(X,4866,'direct'); add(X,4734,'direct',tip='前面的「丁奇·斯迪波爾」只是冬泉谷的引導任務')
add(X,5127,'direct')
add(X,4742,'inside',npc='裂盾滲透者',**IN); add(X,4743,'inside',npc='裂盾滲透者',**IN,note='接在第一個「晉升印章」之後')
add(X,4867,'inside',npc='瓦羅什',**IN); add(X,5047,'inside',npc='芬克·恩霍爾',**IN)
add(X,5103,'inside',npc='物件：人類遺骸',**IN); add(X,5160,'inside',npc='奧比',**IN)
add(X,7761,'inside',npc='物品：黑手的命令',w='副本內掉落',note='上層黑石塔的鑰匙任務')
add(X,4788,'chain',src={'q':'失落的摩沙魯石板','npc':'勘查員詹斯·鐵靴','w':'塔納利斯 (66.8, 24.0)','path':'失落的摩沙魯石板 → 最後的石板'})
GH='布德利是鬼魂，要帶「超維度幽靈顯形器」才看得到'
add(X,8966,'chain',src={'q':'重要的材料','npc':'布德利','w':'黑石山 (32.2, 25.6)','path':'重要的材料 → 瓦薩拉克護符的左半塊'},tip=GH)
add(X,8989,'chain',src={'q':'更多重要的材料','npc':'布德利','w':'黑石山 (32.2, 25.6)','path':'更多重要的材料 → 瓦薩拉克護符的右半塊'},tip=GH)
add(X,8995,'skip',reason='要先交右半塊並做完「最後的準備」，得再打一趟')
add(X,8996,'skip',reason='召喚瓦薩拉克之後的回報任務')
add(X,4735,'skip',reason='要先交「冷凍龍蛋」才接得到，得再打一趟')
add(X,4907,'skip',reason='冬泉谷的傳話任務，沒有副本目標')
def apply(path):
    s=open(path).read()
    if '黑石塔 ----' not in s:
        st=s.index('const QUESTS = [');en=s.index('\n];',st)
        lines=['  {'+','.join(f'{k}:{json.dumps(v,ensure_ascii=False)}' for k,v in e.items())+'},' for e in A]
        s=s[:en]+'\n  /* ---- 黑石塔 ---- */\n'+'\n'.join(lines)+s[en:]
    m=re.search(r'const PENDING_Q = (\{.*?\});',s,flags=re.S)
    p=json.loads(m.group(1)); p.pop('brs',None)
    s=s[:m.start()]+'const PENDING_Q = '+json.dumps(p,ensure_ascii=False,separators=(',',':'))+';'+s[m.end():]
    open(path,'w').write(s)
print(len(A))
for p in sys.argv[1:]: apply(p); print('ok',p)

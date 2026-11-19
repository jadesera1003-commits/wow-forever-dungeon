import os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json,re,sys
Q=os.path.join(ROOT,'data/quests/')
D={}
for i in (1,2,3,4,5): D.update(json.load(open(Q+f'details2_{i}.json')))
SIDE={'聯盟':'A','部落':'H','雙方':'B'}
def loc(v): return f"{v[9]} ({v[10][0]:.1f}, {v[10][1]:.1f})"
A=[]
def add(d,i,c,**k):
    v=D[str(i)]; e={'d':d,'c':c,'n':v[0],'lv':v[1]}
    if v[11]: e['xp']=v[11]
    if c in('direct','chain') and v[10]: e['npc']=v[4]; e['w']=loc(v)
    e.update(k); e['side']=SIDE[v[3]]; e['id']=i; A.append(e)
X='brd'
# Horde
add(X,3981,'direct',tip='到副本監獄區找哥沙克對話')
add(X,4081,'direct',npc='通緝告示'); add(X,4082,'direct',npc='通緝告示')
add(X,4134,'direct',n='遺失的雷酒秘方',en='Lost Thunderbrew Recipe',tip='前面的「薇薇安·拉格雷」只是幽暗城的引導任務')
add(X,7201,'direct'); add(X,97197,'direct')
add(X,3982,'inside',npc='指揮官哥沙克',w='副本監獄區')
add(X,4001,'inside',npc='指揮官哥沙克',w='副本監獄區',note='回奧格瑪交給索爾')
add(X,3907,'chain',src={'q':'不和諧的烈焰','npc':'桑德哈特','w':'荒蕪之地・卡加斯 (3.4, 48.2)','path':'不和諧的烈焰 → 不和諧的火焰'})
add(X,4063,'chain',src={'q':'機器的崛起（第 1 步）','npc':'魯特維爾·沃拉圖斯','w':'荒蕪之地 (25.8, 45.0)','path':'機器的崛起（第 1 步，荒蕪之地）→ 本任務'})
add(X,4132,'chain',src={'q':'格拉克·洛克魯布','npc':'雷克斯洛特','w':'荒蕪之地・卡加斯 (5.8, 47.6)','path':'格拉克·洛克魯布（燃燒平原）→ 押送囚徒 → 行動：殺死安格弗將軍'})
add(X,4002,'skip',reason='索爾的傳話任務，沒有副本目標')
add(X,4003,'skip',reason='要先在副本裡做完哥沙克那幾步、回奧格瑪報告索爾，得再打一趟')
add(X,4004,'skip',reason='救出公主之後的回報任務，接在「拯救公主」後面')
add(X,4122,'skip',reason='目標在燃燒平原，不在副本內'); add(X,4121,'skip',reason='在燃燒平原護送，不在副本內')
add(X,4133,'skip',reason='幽暗城的傳話任務，沒有副本目標')
# Alliance
add(X,4126,'direct',tip='前面的「拉格納·雷酒」只是詛咒之地的引導任務')
add(X,4286,'direct'); add(X,4341,'direct',tip='到副本裡找卡蘭·巨錘對話')
add(X,4242,'inside',npc='溫德索爾元帥',w='副本監獄區',note='交給燃燒平原的麥克斯韋爾元帥')
add(X,4264,'inside',npc='物品：弄皺的便箋',w='副本內黑鐵矮人掉落',note='做完「被遺棄的希望」才會掉')
add(X,4282,'inside',npc='溫德索爾元帥',w='副本監獄區')
add(X,4322,'inside',npc='溫德索爾元帥',w='副本監獄區',note='護送溫德索爾出副本')
add(X,4342,'inside',npc='卡蘭·巨錘',w='副本監獄區')
add(X,4361,'inside',npc='卡蘭·巨錘',w='副本監獄區',note='回鐵爐堡交給麥格尼')
add(X,4241,'chain',src={'q':'黑龍的威脅','npc':'赫林迪斯·河角','w':'燃燒平原・摩根的崗哨 (85.6, 69.0)','path':'黑龍的威脅 → 真正的主人（六步）→ 溫德索爾元帥'})
add(X,4263,'chain',src={'q':'征服者派隆','npc':'加琳達','w':'燃燒平原 (85.4, 70.0)','path':'征服者派隆（燃燒平原的火元素）→ 伊森迪奧斯！'})
add(X,4362,'skip',reason='要先在副本找卡蘭、回鐵爐堡報告麥格尼，得再打一趟')
add(X,4363,'skip',reason='救出公主之後的回報任務')
add(X,4128,'skip',reason='詛咒之地的傳話任務，沒有副本目標')
# Both
add(X,3802,'direct',tip='先跟弗蘭克羅恩對話完成「黑鐵的遺產」第 1 步，再接這個')
add(X,4123,'direct')
add(X,4083,'inside',npc='物件：鬼魂之杯',w='副本內')
add(X,4201,'inside',npc='娜瑪拉小姐',w='副本・黑鐵酒吧')
add(X,82062,'inside',npc='副本內開始',w='副本內開始')
add(X,4024,'chain',src={'q':'烈焰精華（第 1 步）','npc':'塞勒斯·薩雷芬圖斯','w':'燃燒平原 (94.8, 31.6)','path':'烈焰精華（第 1 步）→ 烈焰精華'})
add(X,4136,'chain',src={'q':'尤卡·斯庫比格特','npc':'尤爾巴·斯庫比格特','w':'塔納利斯 (67.0, 24.0)','path':'尤卡·斯庫比格特 → 雷布里·斯庫比格特'})
add(X,3801,'skip',reason='跟弗蘭克羅恩對話的第 1 步，沒有副本目標')
add(X,4324,'skip',reason='塔納利斯的傳話任務，沒有副本目標')
add(X,3911,'skip',reason='「最後的元素」的另一個版本，部落版在上面')
def apply(path):
    s=open(path).read()
    if '黑石深淵 ----' not in s:
        st=s.index('const QUESTS = [');en=s.index('\n];',st)
        lines=['  {'+','.join(f'{k}:{json.dumps(v,ensure_ascii=False)}' for k,v in e.items())+'},' for e in A]
        s=s[:en]+'\n  /* ---- 黑石深淵 ---- */\n'+'\n'.join(lines)+s[en:]
    m=re.search(r'const PENDING_Q = (\{.*?\});',s,flags=re.S)
    p=json.loads(m.group(1)); p.pop('brd',None)
    s=s[:m.start()]+'const PENDING_Q = '+json.dumps(p,ensure_ascii=False,separators=(',',':'))+';'+s[m.end():]
    open(path,'w').write(s)
print(len(A))
for p in sys.argv[1:]: apply(p); print('ok',p)

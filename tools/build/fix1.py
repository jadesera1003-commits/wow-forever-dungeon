import os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
E={e['id']:e for e in json.load(open(os.path.join(ROOT,'data/gen/auto1.json')))}
def S(i,**k):
    e=E[i]
    for a,b in k.items():
        if b is None: e.pop(a,None)
        else: e[a]=b
def direct(i,note=None):
    S(i,c='direct',src=None); 
    if note: S(i,tip=note)
def skip(i,r): S(i,c='skip',reason=r)
# optional breadcrumbs -> direct
direct(2040,'前置「沉默的舒尼」只是引導任務，可以直接找舒尼接')
direct(2922,'「工匠大師歐沃斯巴克」只是暴風城的引導任務，直接找歐沃斯巴克就能接')
direct(2924,'「幫助科勞莫特」是達納蘇斯的引導任務，直接找科羅莫特就能接')
direct(2930,'「卡斯派普的任務」是石爪山脈的引導任務，直接找卡斯派普就能接')
direct(1275,'「遙遠的旅途」只是引導任務，直接找戈沙拉就能接')
# Unsent letter: drop from VanCleef
S(373,c='inside',npc='物品：未寄出的信',w='艾德溫·范克里夫掉落',note='交給暴風城的巴基爾·斯瑞德',reason=None)
S(391,src={'q':'未寄出的信','npc':'艾德溫·范克里夫（死亡礦坑首領掉落）','w':'死亡礦坑','path':'未寄出的信 → 巴基爾·斯瑞德 → 監獄暴動'})
skip(80324,'Wowhead 尚無任務資料')
# Uldaman
S(721,c='chain',src={'q':'一線希望（地圖物品）','npc':'物品：皺巴巴的地圖','w':'荒蕪之地・奧達曼外面的挖掘場','path':'撿到地圖 → 勘察員雷杜爾 → 本任務'})
S(722,src={'q':'一線希望（地圖物品）','npc':'物品：皺巴巴的地圖','w':'荒蕪之地・奧達曼外面的挖掘場','path':'一線希望 → 一線希望 → 鐵趾的護符'})
S(2198,note='交給鐵爐堡的塔瓦斯德·基瑟爾 (36.0, 4.0)')
for i in (2199,2200,2201,2361): skip(i,'項鏈任務鏈要先回鐵爐堡交「破碎的項鏈」才接得到，得再打一趟')
skip(3375,'前置不明，待確認')
S(2398,c='direct',reason=None,npc='勘察員塔伯斯·雷矛',w='鐵爐堡 (74.4, 12.0)',note='在奧達曼裡找到巴爾洛戈')
S(2240,tip='做完「失蹤的矮人」後，在副本裡向巴爾洛戈接')
# RFD Shen'dralar
hub={'q':'林地之語','npc':'米瑟菈','w':'申德拉斯 (53.0, 75.8)','path':'林地之語 → 腐敗與懊悔 → 難辭其咎 → 阿迦瑪甘之血','warn':'要先解鎖申德拉斯營地'}
S(93604,npc='申德拉斯營地 NPC',src=hub)
S(93606,npc='申德拉斯營地 NPC',c='chain',src={**hub,'path':'先解鎖申德拉斯營地'})
# Kroldok
S(94980,n='克羅多克模具',en="Krol'dok Moulding",note='交給大河林地的阿爾馮斯‧仲馬 (64.4, 82.0)')
skip(94981,'「克羅多克模具」在副本內開始，交完才接得到，得再打一趟')
S(94981,n='鑰匙材料',en='Key Ingredients')
S(94983,n='暮光紀念物',en='Twilight Mementos')
S(94997,n='殘留精華',en='Lingering Essence',c='chain',src={'q':'暮光紀念物','npc':'瑞夫坦中士','w':'大河林地 (30.6, 49.0)','path':'暮光紀念物 → 殘留精華'})
S(94998,n='引發好奇心的珍品',en='Curios of Curiosity',c='chain',src={'q':'暮光紀念物','npc':'瑞夫坦中士','w':'大河林地 (30.6, 49.0)','path':'暮光紀念物 → 殘留精華 → 引發好奇心的珍品'})
S(94984,n='暮光典籍',en='Tome of Twilight',c='chain',src={'q':'幫個小忙','npc':'NPC 待查','w':'大河林地','path':'幫個小忙 → 暮光典籍'})
S(94982,en='Eye of Mugg'); S(96771,en='Vengeance of the Highborne')
for i in (95787,95788,97130): S(i,en=E[i]['n'])
# Wetlands dig
S(95810,c='inside',npc='物品開始',w='副本內開始',note='交給濕地的勘察員維爾加 (38.8, 52.2)',reason=None)
S(98824,n='史前稜石',en='Prehistoric Prism'); skip(98824,'要先交副本內掉落開始的「肩負失落聖物」才接得到，得再打一趟')
json.dump(list(E.values()),open(os.path.join(ROOT,'data/gen/fixed1.json'),'w'),ensure_ascii=False)
from collections import Counter;print(Counter(e['c'] for e in E.values()))

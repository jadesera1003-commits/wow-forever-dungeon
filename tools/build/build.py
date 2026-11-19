import os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json,sys,re
Q=os.path.join(ROOT,'data/quests/')
det={}
for i in range(1,6):
    d=json.load(open(Q+f'details_{i}.json'))
    for k,v in d.items():
        if isinstance(v,dict):
            v=[v['t'],v['lv'],v['req'],v['side'],v['start'],v['st'],v['end'],v['ns'],v.get('cls',''),v['series'],v['zone'],v['coord'],v['xp']]
        det[k]=v
obj=json.load(open(Q+'objectives.json'))
dmap={}
for d in ['thanes','dm','stocks','rfd']:
    for q in json.load(open(Q+d+'.json')): dmap[str(q[0])]=d
for d,qs in json.load(open(Q+'alliance_partial.json')).items():
    for q in qs: dmap[str(q[0])]=d
byname={}
for k,v in det.items(): byname.setdefault(v[0],[]).append(k)
SIDE={'聯盟':'A','部落':'H','雙方':'B'}
def loc(v):
    return f"{v[10]} ({v[11][0]:.1f}, {v[11][1]:.1f})" if v[11] else None
out=[]
for k,v in det.items():
    n,lv,req,side,start,st,end,ns,cls,ser,zone,coord,xp=v
    d=dmap.get(k,'?')
    e={'d':d,'n':n,'lv':lv,'side':SIDE.get(side,'B'),'id':int(k)}
    if xp: e['xp']=xp
    if k in obj: e['note']=obj[k][1]
    idx=ser.index(n) if n in ser else -1
    if xp is not None and xp<1000:
        e['c']='skip'; e['reason']='傳話任務，沒有副本目標'+(f'（引導到「{ser[idx+1]}」）' if 0<=idx<len(ser)-1 else '')
    elif not st or not coord:
        e['c']='inside'; e['npc']=start or '物品開始'; e['w']='副本內開始'
        if end: e.setdefault('note','')
        e['end']=end
    else:
        e['npc']=start; e['w']=loc(v)
        if idx>0:
            e['c']='chain'; head=ser[0]; hk=[x for x in byname.get(head,[]) if x!=k]
            hv=det[hk[0]] if hk else None
            e['src']={'q':head,'npc':(hv[4] if hv else 'NPC 待查'),'w':(loc(hv) if hv and hv[11] else '待查'),'path':' → '.join(ser[:idx+1])}
        else: e['c']='direct'
    out.append(e)
json.dump(out,open(os.path.join(ROOT,'data/gen/auto1.json'),'w'),ensure_ascii=False,indent=0)
from collections import Counter
print(Counter(e['d'] for e in out)); print(Counter(e['c'] for e in out))
for e in sorted(out,key=lambda e:(e['d'],e['c'])):
    print(e['d'],e['c'],e['id'],e['n'],e['side'],e.get('npc',''),e.get('w',''),e.get('src',{}).get('q',''),e.get('reason',''))

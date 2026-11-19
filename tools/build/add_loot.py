import os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json,re,sys
N=os.path.join(ROOT,'data/loot/new/')
keys=sys.argv[1].split(',')
dq=json.load(open(os.path.join(ROOT,'data/dq/dq_names.json')))['items']
for p in sys.argv[2:]:
    s=open(p).read()
    m=re.search(r'const RAW_LOOT = (\{.*?\});\n',s)
    R=json.loads(m.group(1))
    for k in keys:
        rows=json.load(open(N+k+'.json'))
        R[k]=[[r[0],dq.get(str(r[0]),r[1]),r[2],r[3],r[4],r[5],r[6],r[7],'',r[8]] for r in rows]
    s=s[:m.start()]+'const RAW_LOOT = '+json.dumps(R,ensure_ascii=False,separators=(',',':'))+';\n'+s[m.end():]
    open(p,'w').write(s); print(p,{k:len(R[k]) for k in keys})

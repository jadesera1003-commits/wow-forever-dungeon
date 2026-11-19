import os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json,re,sys
dq=json.load(open(os.path.join(ROOT,'data/dq/dq_names.json')))
Q,I=dq['quests'],dq['items']
MAN={"Krol'dok Moulding":'94973',"A Token of Vengeance":'94975',"The New Plague":'95216',"Tome of Twilight":'94972',"Crest of Lordaeron":'95204',"Opportunistic Education":'96987',"Elder Knowledge":'95664',"Key Ingredients":'94974',"Eye of Mugg":'94968'}
for p in sys.argv[1:]:
    s=open(p).read(); c=[0,0,0]
    def qfix(m):
        line=m.group(0); i=m.group(2)
        if i in Q and Q[i]!=m.group(1): c[0]+=1; return line.replace(f'n:"{m.group(1)}"',f'n:"{Q[i]}"',1)
        return line
    s=re.sub(r'n:"([^"]*)"[^\n]*?\bid:(\d+)\}',qfix,s)
    def tfix(m):
        en=m.group(2)
        if en in MAN and MAN[en] in Q: c[1]+=1; return f'n:"{Q[MAN[en]]}",en:"{en}"'
        return m.group(0)
    s=re.sub(r'n:"([^"]*（暫譯）[^"]*)",en:"([^"]*)"',tfix,s)
    # items in RAW_LOOT rows: [id,"name",...
    st=s.index('RAW_LOOT'); 
    def ifix(m):
        i=m.group(1)
        if i in I and I[i]!=m.group(2): c[2]+=1; return f'[{i},"{I[i]}"'
        return m.group(0)
    s=s[:st]+re.sub(r'\[(\d+),"([^"]*)"',ifix,s[st:])
    open(p,'w').write(s); print(p,'quests',c[0],'tmp',c[1],'items',c[2])

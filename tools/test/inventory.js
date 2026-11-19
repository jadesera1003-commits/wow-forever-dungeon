const fs=require('fs');const s=fs.readFileSync(process.argv[2],'utf8');
const grab=(name)=>{const i=s.indexOf('const '+name+' = ');const st=s.indexOf((name=='QUESTS'||name=='DUNGEONS')?'[':'{',i);let d=0,e=st;for(;e<s.length;e++){const c=s[e];if(c=='['||c=='{')d++;else if(c==']'||c=='}'){d--;if(!d)break}}return eval('('+s.slice(st,e+1)+')')};
const D=grab('DUNGEONS'),Q=grab('QUESTS'),R=grab('RAW_LOOT');let L={};try{L=grab('LOOT')}catch(e){}
const rows=[];for(const d of D){const q=Q.filter(x=>x.d==d.id);const c=k=>q.filter(x=>x.c==k).length;const loot=(R[d.id]||[]).length+((L[d.id]&&L[d.id].bosses)?L[d.id].bosses.reduce((a,b)=>a+(b.items||[]).length,0):0);
rows.push([d.id,d.name,q.length,c('direct'),c('inside'),c('chain'),c('skip'),q.filter(x=>x.note).length,q.filter(x=>JSON.stringify(x).includes('待查')).length,loot,(R[d.id]||[]).filter(r=>!r[9]).length])}
console.log('id name quests direct inside chain skip withNote 待查 loot loot_noboss');rows.forEach(r=>console.log(r.join(' ')));
console.log('total quests',Q.length,'loot',Object.values(R).reduce((a,b)=>a+b.length,0));

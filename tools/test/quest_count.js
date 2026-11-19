const {JSDOM}=require('jsdom');const fs=require('fs');
const html=fs.readFileSync(process.argv[2],'utf8').replace(/<script src=[^>]*><\/script>/g,'');
const dom=new JSDOM(html,{runScripts:'dangerously',url:'https://x.test/'});
const w=dom.window;
w.localStorage.setItem('dq-who',JSON.stringify(JSON.parse(process.argv[3])));
w.eval('who=JSON.parse(localStorage.getItem("dq-who"))');
const ids=w.eval('DUNGEONS.map(d=>d.id)');
let bad=[];
for(const id of ids){ for(const v of ['quests','loot']){ try{ w.eval(`current=${JSON.stringify(id)};view=${JSON.stringify(v)};render()`); const n=w.document.querySelectorAll(v==='loot'?'.item':'.qcard').length; if(v==='quests') process.stdout.write(id+':'+n+' '); }catch(e){bad.push(id+'/'+v+': '+e.message);} } }
console.log('\nerrors:',bad);

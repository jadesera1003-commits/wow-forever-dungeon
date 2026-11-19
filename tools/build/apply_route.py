"""在副本頁加上「出發前路線」：先去 A 接 X → 去 B 接 Y → 去 C 做前置 → 進副本（可重複執行）。"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSS = '''/*ROUTE-BEGIN*/
details.route{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin:0 0 12px}
details.route summary{cursor:pointer;font-weight:700;font-size:14px}
details.route ol{margin:8px 0 2px;padding-left:22px;display:flex;flex-direction:column;gap:8px;font-size:14px;line-height:1.55}
details.route ul.rl{margin:2px 0 0;padding-left:16px;list-style:disc}
details.route .rz{font-weight:700}
details.route .rq{color:var(--ink)}
details.route .rs{color:var(--muted);font-size:12.5px}
details.route .rh{font-size:12.5px;color:var(--muted);margin:8px 0 0}
details.route .long{margin-top:8px;font-size:13px;border-top:1px dashed var(--line);padding-top:6px}
details.route .long b{color:#ffb347}
/*ROUTE-END*/'''
JS = r'''
<script id="route-js">
(function(){
  const CAP = {H:["奧格瑪","雷霆崖","幽暗城"], A:["暴風城","鐵爐堡","達納蘇斯"]};
  const zoneOf = w => (w || "").split(/[・(（]/)[0].trim();
  const isGate = w => /副本|入口/.test(w || "");
  function chainInfo(q){
    const qs = q.id && QS[q.id];
    if (qs) return "這串共 " + qs.s.length + " 步，副本任務是第 " + (qs.p + 1) + " 步";
    if (q.src && q.src.path){ const n = q.src.path.split("→").length; return n > 1 ? "這串共 " + n + " 步，副本任務是第 " + n + " 步" : ""; }
    return "";
  }
  function buildRoute(d, all){
    const qs = all.filter(q => q.c === "direct" || q.c === "chain");
    const stops = new Map(), deps = [];
    const zkey = w => isGate(w) ? "副本門口" : (zoneOf(w) || "其他");
    const clean = n => (n || "").replace(/（暫譯）/g, "");
    const put = (w, line) => { const z = zkey(w); if (!stops.has(z)) stops.set(z, {t: [], sub: new Set()}); const s = stops.get(z); s.t.push(line);
      const sub = (w || "").replace(zoneOf(w), "").replace(/^・/, "").replace(/[（(][^)）]*[)）]/g, "").trim(); if (sub && z !== "副本門口") s.sub.add(sub); };
    qs.forEach(q => {
      const info = chainInfo(q);
      if (q.c === "chain" && q.src){
        const npc = q.src.npc && !/待查/.test(q.src.npc) ? "找" + clean(q.src.npc) + "接" : "接";
        put(q.src.w, [npc + "「" + q.src.q + "」", "一路做到「" + q.n + "」" + (info ? "（" + info + "）" : "")]);
        deps.push([zkey(q.src.w), zkey(q.w)]);
      } else {
        const npc = !q.npc || /^物品|NPC|待查/.test(q.npc) ? "接" : /告示|佈告|公告/.test(q.npc) ? "看" + clean(q.npc) + "接" : "找" + clean(q.npc) + "接";
        put(q.w, [npc + "「" + q.n + "」", info]);
      }
    });
    const caps = CAP[who.f] || [];
    const rank = z => z === "副本門口" ? 9 : caps.includes(z) ? caps.indexOf(z) : 5;
    let order = [...stops.keys()].sort((a, b) => rank(a) - rank(b) || stops.get(b).t.length - stops.get(a).t.length);
    for (let k = 0; k < 5; k++) deps.forEach(([h, t]) => { const i = order.indexOf(h), j = order.indexOf(t); if (h !== t && i > j && h !== "副本門口"){ order.splice(i, 1); order.splice(j, 0, h); } });
    const box = document.createElement("details"); box.className = "route";
    const sm = document.createElement("summary"); sm.textContent = "出發前路線：要接 " + qs.length + " 個任務，跑 " + order.length + " 個地方"; box.appendChild(sm);
    const ol = document.createElement("ol");
    order.forEach(z => {
      const li = document.createElement("li"); const s = stops.get(z);
      const head = document.createElement("div"); head.className = "rz";
      head.textContent = (z === "副本門口" ? "副本門口" : z) + (s.sub.size ? "（" + [...s.sub].join("、") + "）" : "");
      li.appendChild(head);
      const ul = document.createElement("ul"); ul.className = "rl";
      s.t.forEach(([main, sub]) => { const x = document.createElement("li"); x.textContent = main; if (sub){ const y = document.createElement("span"); y.className = "rs"; y.textContent = "　" + sub; x.appendChild(y); } ul.appendChild(x); });
      li.appendChild(ul); ol.appendChild(li);
    });
    const ins = all.filter(q => q.c === "inside");
    const li = document.createElement("li"); const hd = document.createElement("div"); hd.className = "rz"; hd.textContent = "進副本"; li.appendChild(hd);
    if (ins.length){ const ul = document.createElement("ul"); ul.className = "rl"; ins.forEach(q => { const x = document.createElement("li"); x.textContent = "副本內接「" + q.n + "」"; const inf = chainInfo(q); if (inf){ const y = document.createElement("span"); y.className = "rs"; y.textContent = "　" + inf; x.appendChild(y); } ul.appendChild(x); }); li.appendChild(ul); }
    ol.appendChild(li);
    box.appendChild(ol);
    const hnt = document.createElement("p"); hnt.className = "rh"; hnt.textContent = "地點順序是粗排，可依你的爐石和飛行點調整。";
    box.appendChild(hnt);
    return box;
  }
  const _rd = renderDungeon;
  renderDungeon = function(){
    _rd();
    if (view === "loot") return;
    const cols = main.querySelector(".cols"); if (!cols) return;
    const d = DUNGEONS.find(x => x.id === current);
    const all = QUESTS.filter(q => q.d === d.id && avail(q));
    { const vis = new Set(all.map(q => q.id)); for (let i = all.length - 1; i >= 0; i--){ const hd = all[i].id && QFOLD[all[i].id]; if (hd && vis.has(hd) && all[i].c !== "skip") all.splice(i, 1); } }
    const anchor = main.querySelector(".expall") || cols;
    anchor.before(buildRoute(d, all));
  };
  render();
})();
</script>
'''
for p in ['index.html', 'claude-artifact/index.html']:
    path = os.path.join(ROOT, p); h = open(path, encoding='utf-8').read()
    h = re.sub(r'/\*ROUTE-BEGIN\*/.*?/\*ROUTE-END\*/', '', h, flags=re.S)
    h = re.sub(r'\n<script id="route-js">.*?</script>\n', '', h, flags=re.S)
    h = h.replace('</style>', CSS + '</style>', 1)
    i = h.rindex('</body>'); h = h[:i] + JS + h[i:]
    open(path, 'w', encoding='utf-8').write(h); print(p, 'route applied')

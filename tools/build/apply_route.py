"""在副本頁加上「出發前路線」：先去 A 接 X → 去 B 接 Y → 去 C 做前置 → 進副本（可重複執行）。"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSS = '''/*ROUTE-BEGIN*/
details.route{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin:0 0 12px}
details.route summary{cursor:pointer;font-weight:700;font-size:14px}
details.route ol{margin:8px 0 2px;padding-left:22px;display:flex;flex-direction:column;gap:6px;font-size:14px;line-height:1.55}
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
  function buildRoute(d, all){
    const qs = all.filter(q => q.c === "direct" || q.c === "chain");
    const stops = new Map(), long = [], deps = [];
    const zkey = w => isGate(w) ? "副本門口" : (zoneOf(w) || "其他");
    const put = (w, txt) => { const z = zkey(w); if (!stops.has(z)) stops.set(z, {t: [], sub: new Set()}); const s = stops.get(z); s.t.push(txt);
      const sub = (w || "").replace(zoneOf(w), "").replace(/^・/, "").replace(/[（(][^)）]*[)）]/g, "").trim(); if (sub && z !== "副本門口") s.sub.add(sub); };
    qs.forEach(q => {
      if (q.c === "chain" && q.src){
        const steps = (q.src.path || "").split("→").length;
        const prev = (q.id && QS[q.id]) ? QS[q.id].p : 0;
        if (steps >= 4 || prev >= 3 || q.src.warn) { long.push(q); return; }
        put(q.src.w, "先做「" + q.src.q + "」（才能接「" + q.n + "」）");
        put(q.w, "接「" + q.n + "」");
        deps.push([zkey(q.src.w), zkey(q.w)]);
      } else put(q.w, "接「" + q.n + "」");
    });
    const caps = CAP[who.f] || [];
    const rank = z => z === "副本門口" ? 9 : caps.includes(z) ? caps.indexOf(z) : 5;
    let order = [...stops.keys()].sort((a, b) => rank(a) - rank(b) || stops.get(b).t.length - stops.get(a).t.length);
    for (let k = 0; k < 5; k++) deps.forEach(([h, t]) => { const i = order.indexOf(h), j = order.indexOf(t); if (h !== t && i > j && h !== "副本門口"){ order.splice(i, 1); order.splice(j, 0, h); } });
    const box = document.createElement("details"); box.className = "route";
    const sm = document.createElement("summary"); sm.textContent = "出發前路線（" + order.length + " 站）"; box.appendChild(sm);
    const ol = document.createElement("ol");
    order.forEach((z, i) => {
      const li = document.createElement("li"); const s = stops.get(z);
      const head = (i === 0 ? "先去" : "再去") + (z === "副本門口" ? "副本門口" : z) + (s.sub.size ? "（" + [...s.sub].join("、") + "）" : "");
      li.innerHTML = '<span class="rz"></span>：<span class="rq"></span>';
      li.querySelector(".rz").textContent = head; li.querySelector(".rq").textContent = s.t.join("、");
      ol.appendChild(li);
    });
    const li = document.createElement("li"); li.innerHTML = '<span class="rz">進副本</span>';
    const ins = all.filter(q => q.c === "inside").length;
    if (ins) li.append("：裡面還能接 " + ins + " 個");
    ol.appendChild(li);
    box.appendChild(ol);
    if (long.length){
      const L = document.createElement("div"); L.className = "long";
      L.innerHTML = "<b>長系列，建議練等時先做：</b>";
      long.forEach(q => { const p = document.createElement("div"); const qs = q.id && QS[q.id];
        p.textContent = qs && qs.p >= 3 ? "・「" + q.n + "」：從「" + qs.s[0][1] + "」開始，前面還有 " + qs.p + " 步"
          : "・「" + q.n + "」：從「" + q.src.q + "」開始（" + q.src.npc + "，" + zoneOf(q.src.w) + "）";
        L.appendChild(p); });
      box.appendChild(L);
    }
    const hnt = document.createElement("p"); hnt.className = "rh"; hnt.textContent = "順序依區域粗排，可依你的爐石和飛行點調整。";
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

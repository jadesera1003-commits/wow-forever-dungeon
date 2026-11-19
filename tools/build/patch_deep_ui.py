import sys
JS = r'''
  const qx = q.id && QX[q.id];
  if (qx){
    if (qx.o && qx.o !== q.note){ const o = document.createElement("div"); o.className = "blk obj"; add(o, "lab", "任務目標"); o.append(qx.o); el.appendChild(o); }
    if (qx.g || qx.c){
      const r = document.createElement("div"); r.className = "blk rew"; add(r, "lab", "任務獎勵");
      const grp = (ids, lab) => {
        const w = add(r, "rg", ""); add(w, "rl", lab);
        ids.forEach(id => {
          const it = RIT[id]; const a = document.createElement("a");
          a.className = "ri q" + (it ? it[1] : 1); a.href = "https://www.wowhead.com/forever/tw/item=" + id; a.target = "_blank"; a.rel = "noopener";
          a.textContent = it ? it[0].replace(/^\[(.*)\]$/, "$1") : ("物品 #" + id);
          if (it && it[2]){ const s = document.createElement("span"); s.className = "rt"; s.textContent = it[2]; a.appendChild(s); }
          const ok = rewUse(it && it[2], q.lv); if (ok === false) a.classList.add("no"); else if (ok === true) a.classList.add("ok");
          w.appendChild(a);
        });
      };
      if (qx.g) grp(qx.g, "固定給"); if (qx.c) grp(qx.c, "擇一");
      el.appendChild(r);
    }
    if (qx.u){
      const u = document.createElement("div"); u.className = "blk unl"; add(u, "lab", "後續解鎖");
      qx.u.filter(e => !e[4] || !who.f || e[4] === who.f).forEach(([id, n, tag, note, sd, ug, uc]) => {
        const line = add(u, "ul", "");
        const c = document.createElement("span"); c.className = "tag t-" + tag; c.textContent = UNL_TAG[tag] || "後續"; line.appendChild(c);
        const a = document.createElement("a"); a.href = "https://www.wowhead.com/forever/tw/quest=" + id; a.target = "_blank"; a.rel = "noopener"; a.textContent = n; line.appendChild(a);
        if (note){ const s = document.createElement("span"); s.className = "un"; s.textContent = note; line.appendChild(s); }
        if (tag === "main" && QFOLD[id] && QX[id] && QX[id].o){ const s = document.createElement("div"); s.className = "uo"; s.textContent = QX[id].o; u.appendChild(s); }
        [[ug, "固定給"], [uc, "擇一"]].forEach(([ids, lab]) => {
          if (!ids || !ids.length) return;
          const w2 = add(u, "rg", ""); add(w2, "rl", lab);
          ids.forEach(iid => { const it = RIT[iid]; const a = document.createElement("a");
            a.className = "ri q" + (it ? it[1] : 1); a.href = "https://www.wowhead.com/forever/tw/item=" + iid; a.target = "_blank"; a.rel = "noopener";
            a.textContent = it ? it[0].replace(/^\[(.*)\]$/, "$1") : ("物品 #" + iid);
            if (it && it[2]){ const s = document.createElement("span"); s.className = "rt"; s.textContent = it[2]; a.appendChild(s); }
            const ok = rewUse(it && it[2], q.lv); if (ok === false) a.classList.add("no"); else if (ok === true) a.classList.add("ok");
            w2.appendChild(a); });
        });
      });
      el.appendChild(u);
    }
  }
'''
FN = r'''
const UNL_TAG = {main:"副本任務", imp:"重要系列", gear:"有獎勵", end:"收尾／對話", next:"後續"};
/* 任務獎勵能不能用：ty 是「部位 類型」字串，回傳 true／false／null */
function rewUse(ty, lv){
  if (!ty || !who.c) return null;
  const w = ty.split(" "); const slot = w[0], k = w[1] || "";
  const map = {"板甲":"鎧甲","盾":"盾牌","權杖":slot==="雙手"?"雙手錘":"錘","斧":slot==="雙手"?"雙手斧":"斧","劍":slot==="雙手"?"雙手劍":"劍"};
  let t = map[k] || k;
  if (!t) t = {"背部":"背部","手指":"戒指","頸部":"項鍊","飾品":"飾品","副手物品":"副手物品"}[slot] || "其他";
  if (t === "限職業") return null;
  return canUse({t, req: lv});
}
'''
CSS = '''.qcard .blk.rew .rg{display:flex;flex-wrap:wrap;gap:4px 6px;align-items:baseline;margin-top:2px}
.qcard .blk.rew .rl{font-size:12px;color:var(--muted);margin-right:2px}
.qcard .ri{--qc:#e8e8e8;color:var(--qc);text-decoration:none;font-weight:600;border:1px solid var(--line);border-radius:5px;padding:1px 7px;background:var(--panel)}
.qcard .ri.q2{--qc:#4dff5e}.qcard .ri.q3{--qc:#4fa8ff}.qcard .ri.q4{--qc:#c47dff}
.qcard .ri .rt{font-weight:400;font-size:11px;color:var(--muted);margin-left:5px}
.qcard .ri.ok{border-color:var(--qc)}.qcard .ri.no{opacity:.45}
.qcard .blk.unl .ul{display:flex;flex-wrap:wrap;gap:4px 8px;align-items:baseline}
.qcard .blk.unl a{color:var(--ink)}
.qcard .blk.unl .un{font-size:12px;color:var(--muted)}
.qcard .tag{font-size:11px;font-weight:700;padding:0 6px;border-radius:999px;border:1px solid currentColor;color:var(--muted)}
.qcard .tag.t-main{color:var(--chain)}.qcard .tag.t-imp{color:#ffb347}.qcard .tag.t-gear{color:#4fa8ff}
'''
for path in sys.argv[1:]:
    h = open(path, encoding='utf-8').read()
    if 'function rewUse' in h: print(path, 'already'); continue
    anchor = '  if (q.note){ const n = document.createElement("p"); n.className = "note"; n.textContent = q.note; el.appendChild(n); }\n'
    assert anchor in h, path
    h = h.replace(anchor, anchor + JS.lstrip('\n'), 1)
    h = h.replace('function card(q, showDungeon){', FN.lstrip('\n') + 'function card(q, showDungeon){', 1)
    a2 = '.qcard .blk .lab{'
    i = h.index(a2); j = h.index('\n', i) + 1
    h = h[:j] + CSS + h[j:]
    open(path, 'w', encoding='utf-8').write(h); print(path, 'patched')

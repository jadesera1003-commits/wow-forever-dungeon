"""套用正式排版：分組清單、任務預設收成一行、獎勵只顯示圖示（可重複執行，以 FOLD-BEGIN/END 標記）。"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSS = '''/*FOLD-BEGIN*/
.qcard.fold{gap:4px;cursor:default}
.qcard.fold .qh{cursor:pointer}
.qcard .sum{font-size:13px;color:var(--muted);cursor:pointer}
.qcard .chips{display:flex;flex-wrap:wrap;gap:4px;margin-top:2px;cursor:pointer}
.qcard .chip2{font-size:11.5px;padding:1px 7px;border-radius:999px;border:1px solid var(--line);color:var(--muted);background:var(--panel-2)}
.qcard .chip2.g{color:#4fa8ff;border-color:#4fa8ff55}.qcard .chip2.w{color:#ffb347;border-color:#ffb34766}.qcard .chip2.p{color:var(--chain);border-color:currentColor}
.qcard .tog{font-size:12px;color:var(--muted);margin-top:2px;cursor:pointer;user-select:none}
.qcard.fold .det{display:none}
.qcard.fold.open .det{display:flex;flex-direction:column;gap:8px;margin-top:6px}
.qcard.fold.open .sum,.qcard.fold.open .chips{display:none}
.rw-c .ri{padding:2px;border-radius:6px;background:none;min-width:30px;min-height:30px;display:inline-flex;align-items:center;justify-content:center}
.rw-c .ri .rn,.rw-c .ri .rt{display:none}
.rw-c .ri:not(:has(.iconmedium,.iconsmall,span[class^=icon])) .rn{display:inline;font-size:0}
.rw-c .ri:not(:has(.iconmedium,.iconsmall,span[class^=icon]))::before{content:attr(data-a);font-size:13px;font-weight:700;color:var(--qc);width:26px;height:26px;display:grid;place-items:center;border:2px solid var(--qc);border-radius:5px}
.rw-c .ri.no{opacity:.35}
.rw-c .hint{font-size:11.5px;color:var(--muted);margin-top:2px}
.cols{grid-template-columns:minmax(0,1fr)!important;display:grid;gap:14px}
.col .cards{gap:6px}
.qcard.fold:not(.open){padding:8px 12px}
.qcard.fold:not(.open) .sum,.qcard.fold:not(.open) .tog{display:none}
.qcard.fold:not(.open) .qh .en{display:none}
.qcard.fold:not(.open) .qh .t{font-size:15px}
.qcard.fold .qh::after{content:"▾";color:var(--muted);font-size:12px;margin-left:6px;align-self:center}
.qcard.fold.open .qh::after{content:"▴"}
.expall{margin:0 0 10px;font-size:13px;padding:4px 12px;border-radius:999px;border:1px solid var(--line);background:var(--panel-2);color:var(--ink);cursor:pointer}
.cols{grid-template-columns:1fr!important;max-width:760px}
.col .desc{display:none}
.col h3{margin-bottom:6px}
.cards{gap:6px!important}
.qcard.fold{padding:9px 12px}
.pvbar{display:none}
/*FOLD-END*/'''
JS = r'''
<script id="fold-js">
(function(){
  const _card = card;
  function chips(q){
    const out = [];
    const qs = q.id && QS[q.id], qx = q.id && QX[q.id];
    if (q.c === "chain") out.push(["要先做前置", "p"]);
    if (qs) out.push(["系列 " + (qs.p + 1) + "/" + qs.s.length, ""]);
    const mine = qx && [].concat(qx.g || [], qx.c || []);
    const usable = ids => ids.filter(id => { const it = RIT[id]; return rewUse(it && it[2], q.lv) === true; }).length;
    if (mine && mine.length){
      const n = usable(mine);
      out.push([n ? "獎勵 " + n + " 件可用" : "有獎勵", "g"]);
    } else if (qs && qs.r.length){
      out.push(["獎勵在第 " + (qs.r[qs.r.length - 1][0] + 1) + " 步", "g"]);
    } else if (qs) out.push(["整串只有經驗", ""]);
    if (qs && qs.a.length) out.push(["要再進副本", "w"]);
    if (qx && qx.ns) out.push(["不能分享", "w"]);
    return out;
  }
  function compact(blk){
    blk.querySelectorAll(".ri").forEach(a => {
      const t = a.firstChild;
      if (t && t.nodeType === 3){ const s = document.createElement("span"); s.className = "rn"; s.textContent = t.textContent; a.replaceChild(s, t); a.dataset.a = s.textContent.slice(0, 1); a.title = s.textContent; }
    });
    blk.classList.add("rw-c");
    const h = document.createElement("div"); h.className = "hint"; h.textContent = "點一下顯示名稱"; blk.appendChild(h);
    blk.addEventListener("click", e => {
      if (blk.classList.contains("rw-c")){ e.preventDefault(); blk.classList.remove("rw-c"); h.remove(); }
    }, true);
  }
  card = function(q, sd){
    const el = _card(q, sd);
    const head = el.querySelector(".qh");
    const det = document.createElement("div"); det.className = "det";
    [...el.children].filter(c => c !== head && !c.classList.contains("cat")).forEach(c => det.appendChild(c));
    const sum = document.createElement("div"); sum.className = "sum";
    sum.textContent = (q.npc || "") + (q.w ? "・" + q.w : "");
    const ch = document.createElement("div"); ch.className = "chips";
    chips(q).forEach(([t, k]) => { const s = document.createElement("span"); s.className = "chip2 " + k; s.textContent = t; ch.appendChild(s); });
    const tog = document.createElement("div"); tog.className = "tog"; tog.textContent = "▾ 展開";
    el.append(sum, ch, tog, det);
    el.classList.add("fold");
    det.querySelectorAll(".blk.rew,.blk.ser,.blk.unl").forEach(b => { if (b.querySelector(".ri")) compact(b); });
    const flip = () => { el.classList.toggle("open"); tog.textContent = el.classList.contains("open") ? "▴ 收合" : "▾ 展開"; };
    [head, sum, ch, tog].forEach(x => x.addEventListener("click", flip));
    return el;
  };
  const _rd = renderDungeon;
  renderDungeon = function(){
    _rd();
    const cols = main.querySelector(".cols"); if (!cols) return;
    const b = document.createElement("button"); b.className = "expall"; b.textContent = "全部展開";
    b.onclick = () => { const open = b.textContent === "全部展開"; main.querySelectorAll(".qcard.fold").forEach(c => { c.classList.toggle("open", open); const t = c.querySelector(".tog"); if (t) t.textContent = open ? "▴ 收合" : "▾ 展開"; }); b.textContent = open ? "全部收合" : "全部展開"; };
    cols.before(b);
  };
  render();
})();
</script>
'''
import re
for p in ['index.html', 'claude-artifact/index.html']:
    path = os.path.join(ROOT, p); h = open(path, encoding='utf-8').read()
    h = re.sub(r'/\*FOLD-BEGIN\*/.*?/\*FOLD-END\*/', '', h, flags=re.S)
    h = re.sub(r'\n<script id="fold-js">.*?</script>\n', '', h, flags=re.S)
    h = h.replace('</style>', CSS + '</style>', 1)
    i = h.rindex('</body>')
    h = h[:i] + JS + h[i:]
    open(path, 'w', encoding='utf-8').write(h)
    print(p, 'fold layout applied')

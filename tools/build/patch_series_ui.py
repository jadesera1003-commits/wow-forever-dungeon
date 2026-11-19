"""在任務卡片加上「系列進度」區塊（只需跑一次）。"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = r'''
  const qs = q.id && QS[q.id];
  if (qs){
    const b = document.createElement("div"); b.className = "blk ser";
    add(b, "lab", "系列進度　第 " + (qs.p + 1) + " 步／共 " + qs.s.length + " 步");
    const ch = add(b, "chain", "");
    qs.s.forEach(([id, n, rw], i) => {
      if (i) ch.append(" → ");
      const s = document.createElement(i === qs.p ? "b" : "span"); s.textContent = (i === qs.p ? "▶" : "") + n + (rw && i > qs.p ? " 🎁" : "");
      if (i < qs.p) s.className = "done";
      ch.appendChild(s);
    });
    const mine = qx && (qx.g || qx.c);
    if (qs.r.length){
      qs.r.forEach(([i, npc, w, g, c]) => {
        const r = add(b, "fin", "");
        const t = document.createElement("div"); t.className = "ft";
        t.textContent = "🎁 第 " + (i + 1) + " 步「" + qs.s[i][1] + "」" + (npc ? "交給 " + npc : "") + (w ? "・" + w : "");
        r.appendChild(t);
        [[g, "固定給"], [c, "擇一"]].forEach(([ids, lab]) => {
          if (!ids || !ids.length) return;
          const w2 = add(r, "rg", ""); add(w2, "rl", lab);
          ids.forEach(id => { const it = RIT[id]; const a = document.createElement("a");
            a.className = "ri q" + (it ? it[1] : 1); a.href = "https://www.wowhead.com/forever/tw/item=" + id; a.target = "_blank"; a.rel = "noopener";
            a.textContent = it ? it[0].replace(/^\[(.*)\]$/, "$1") : ("物品 #" + id);
            if (it && it[2]){ const s = document.createElement("span"); s.className = "rt"; s.textContent = it[2]; a.appendChild(s); }
            const ok = rewUse(it && it[2], q.lv); if (ok === false) a.classList.add("no"); else if (ok === true) a.classList.add("ok");
            w2.appendChild(a); });
        });
      });
      if (!mine) add(b, "sn", "這一步只給經驗，物品獎勵在後面");
    } else if (!mine) add(b, "sn", "整串沒有物品獎勵（只有經驗）");
    if (qs.a.length) add(b, "warn", "⚠ 需要再進副本：" + qs.a.map(i => "第 " + (i + 1) + " 步「" + qs.s[i][1] + "」").join("、"));
    else if (qs.o) add(b, "ok2", "後面的步驟都在副本外，出副本就能做完");
    el.appendChild(b);
  }
'''
CSS = '''.qcard .blk.ser .chain{line-height:1.7}.qcard .blk.ser .chain .done{color:var(--muted)}.qcard .blk.ser .chain b{color:var(--ink)}
.qcard .blk.ser .fin{margin-top:4px}.qcard .blk.ser .ft{font-weight:600}
.qcard .blk.ser .sn,.qcard .blk.ser .ok2{font-size:12px;color:var(--muted);margin-top:2px}
.qcard .blk.ser .warn{font-size:12px;color:#ffb347;margin-top:2px}
'''
for p in ['index.html', 'claude-artifact/index.html']:
    path = os.path.join(ROOT, p); h = open(path, encoding='utf-8').read()
    if 'const qs = q.id && QS[q.id]' in h: print(p, 'already'); continue
    anchor = '    if (qx.u){'
    assert anchor in h
    # 系列區塊放在獎勵之後、後續解鎖之前；qx 不存在時也要顯示，所以插在 if(qx) 區塊外面
    end = h.index('  if (q.src){', h.index(anchor))
    h = h[:end] + JS.lstrip('\n') + h[end:]
    i = h.index('.qcard .blk .lab{'); j = h.index('\n', i) + 1
    h = h[:j] + CSS + h[j:]
    open(path, 'w', encoding='utf-8').write(h); print(p, 'patched')

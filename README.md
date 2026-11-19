# WoW Forever 副本任務查詢

依陣營、種族、職業查詢各副本的任務：在哪接、前置系列從哪開始、副本內會拿到哪些任務，以及首領掉落。

網站：https://jadesera1003-commits.github.io/wow-forever-dungeon/

物品圖示與說明框由 [Wowhead](https://www.wowhead.com/forever) 提供。本站為玩家自製的非官方工具，與暴雪娛樂無關。

---

## 資料夾

| 位置 | 內容 |
|---|---|
| `index.html` | 網站本體（GitHub Pages 直接發佈這個檔） |
| `claude-artifact/index.html` | Claude 測試版（沒有 Wowhead 圖示，其餘相同） |
| `data/quests/` | 從 Wowhead 爬的任務資料：各副本任務清單、任務詳情（開始／結束 NPC、座標、系列、經驗） |
| `data/loot/` | 各副本掉落原始資料；`data/loot/new/` 是 50–60 級與 Forever 新副本 |
| `data/dq/` | 遊戲內中文名稱：`dq_names.json`（整理後）、`scans/`（DQNames 插件原始存檔） |
| `data/gen/` | 分類程式的中間檔 |
| `tools/build/` | 整理資料、寫進網站的程式（Python） |
| `tools/test/` | 檢查網站能不能正常顯示的測試（Node.js + jsdom） |
| `addon/DQNames/` | 遊戲內掃描中文名稱的插件原始碼 |

## 資料格式

**任務詳情**（`data/quests/details*.json`），每筆以任務編號為鍵：

```
[名稱, 等級, 需求等級, 陣營, 開始NPC, "npc=編號", 結束NPC, 不可共享(0/1), [系列任務名稱...], 開始地區, [x, y], 經驗]
```

（`details_1.json` 是早期格式，欄位相同但用物件表示）

**掉落**（網站內 `RAW_LOOT`，原始檔在 `data/loot/`）：

```
[物品編號, 名稱, 品質, 大類, 子類, 部位, 需求等級, 來源名稱, Forever 改動, 來源NPC編號]
```

## 常用流程

```bash
# 測試網站（第一次先裝 jsdom）
cd tools/test && npm install && cd ../..
node tools/test/render_test.js index.html
node tools/test/inventory.js index.html      # 各副本任務數、掉落數一覽

# 遊戲內掃描完後，把中文名稱套進網站
python3 tools/build/convert_dqnames.py <DQNames.lua> data/dq/dq_names.json
python3 tools/build/apply_dq.py index.html claude-artifact/index.html
```

## 爬 Wowhead 的規則

- 每頁間隔約 2.5 秒，一次最多 8–9 頁。
- 遇到人機驗證（Human Verification）就停，不要繞過；等 30–60 分鐘，或在瀏覽器手動驗證。
- 爬到的結果要馬上存進 `data/`，再推上 GitHub，避免遺失。

## 深度資料（2026-11-19）
- `data/quests/deep_*.json`、`deep_heads_*.json`：每個任務的 `[前置[], 後續解鎖[], 固定獎勵[], 擇一獎勵[], 任務目標]`，共 431 個（含系列源頭）。
- `data/items/reward_items.json`：任務獎勵物品 `[名稱, 品質, "部位 類型"]`。名稱是 `[English]` 的表示 Wowhead 還沒有中文，等 DQNames 掃描補。
- `tools/build/patch_deep_ui.py`：在任務卡片加上「任務目標／任務獎勵／後續解鎖」區塊（只需跑一次）。
- `tools/build/add_deep.py`：把深度資料注入網站（可重複執行）；後續解鎖的重要程度標籤在檔案內的 `TAG`／`NOTE` 手動維護。
- `tools/build/fix_review.py`：套用 `review_notes.md` 的分類修正。
- `data/quests/series_*.json`：系列資料 `[系列任務ID[], 交任務NPC, [區域,座標], 固定獎勵[], 擇一獎勵[], 目標]`。
- `tools/build/patch_series_ui.py`（跑一次）＋ `tools/build/add_series.py`（可重複）：卡片上的「系列進度」——第幾步、後面哪一步有獎勵、要不要再進副本。
- 建置順序：`add_deep.py` → `add_series.py` → `fix_review.py`（add_deep 會重建 RIT，所以 add_series 要在它後面）。

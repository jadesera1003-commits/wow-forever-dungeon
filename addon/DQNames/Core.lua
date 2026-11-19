-- DQNames：掃描物品、任務、NPC 的中文名稱
-- 指令：/dqscan 開始掃描，/dqscan status 看進度，/dqscan stop 停止，掃完後輸入 /reload 存檔

local ADDON = "DQNames"
local PREFIX = "|cffffd84d[DQNames]|r "
local f = CreateFrame("Frame")

local function say(msg) DEFAULT_CHAT_FRAME:AddMessage(PREFIX .. msg) end

local function initDB()
  DQNamesDB = DQNamesDB or {}
  DQNamesDB.items = DQNamesDB.items or {}
  DQNamesDB.quests = DQNamesDB.quests or {}
  DQNamesDB.npcs = DQNamesDB.npcs or {}
  DQNamesDB.seen = DQNamesDB.seen or {}  -- 遊戲中看到的 NPC：名稱與位置
  DQNamesDB.meta = DQNamesDB.meta or {}
  DQNamesDB.meta.locale = GetLocale()
  local _, build, _, toc = GetBuildInfo()
  DQNamesDB.meta.build = build
  DQNamesDB.meta.interface = toc
end

---------------------------------------------------------------------------
-- 物品：C_Item.GetItemInfo / GetItemInfo，資料沒載入時等 GET_ITEM_INFO_RECEIVED
---------------------------------------------------------------------------
local GetItemInfoCompat = (C_Item and C_Item.GetItemInfo) or GetItemInfo
local function tryItem(id)
  local name = GetItemInfoCompat(id)
  if name then DQNamesDB.items[id] = name; return true end
  return false
end

---------------------------------------------------------------------------
-- 任務：不同版本的 API 名稱不同，依序嘗試
---------------------------------------------------------------------------
local function questTitle(id)
  if C_QuestLog and C_QuestLog.GetTitleForQuestID then
    local t = C_QuestLog.GetTitleForQuestID(id)
    if t and t ~= "" then return t end
  end
  if C_QuestLog and C_QuestLog.GetQuestInfo then
    local t = C_QuestLog.GetQuestInfo(id)
    if t and t ~= "" then return t end
  end
  return nil
end
local function requestQuest(id)
  if C_QuestLog and C_QuestLog.RequestLoadQuestByID then C_QuestLog.RequestLoadQuestByID(id) end
end
local function tryQuest(id)
  local t = questTitle(id)
  if t then DQNamesDB.quests[id] = t; return true end
  requestQuest(id)
  return false
end

---------------------------------------------------------------------------
-- NPC：用隱藏的說明框讀 unit 連結；讀不到就等你在遊戲中選取或滑鼠移過
---------------------------------------------------------------------------
local tip = CreateFrame("GameTooltip", "DQNamesScanTip", UIParent, "GameTooltipTemplate")
tip:SetOwner(UIParent, "ANCHOR_NONE")
local function tryNpc(id)
  tip:ClearLines()
  local ok = pcall(tip.SetHyperlink, tip, ("unit:Creature-0-0-0-0-%d-0000000000"):format(id))
  if ok then
    local line = _G["DQNamesScanTipTextLeft1"]
    local t = line and line:GetText()
    if t and t ~= "" and not t:find("^%s*$") then DQNamesDB.npcs[id] = t; return true end
  end
  return false
end

-- 副本內或戰鬥中，遊戲會把 GUID、名稱變成「保密值」，不能讀取；遇到就跳過，不報錯
local function isSecret(v)
  if issecretvalue then local ok, r = pcall(issecretvalue, v); if not ok or r then return true end end
  if canaccessvalue then local ok, r = pcall(canaccessvalue, v); if not ok or not r then return true end end
  return false
end

local function recordUnitInner(unit)
  if not UnitExists(unit) or UnitIsPlayer(unit) then return end
  local guid = UnitGUID(unit)
  if not guid or isSecret(guid) then return end
  local kind, _, _, _, _, npcID = strsplit("-", guid)
  if kind ~= "Creature" and kind ~= "Vehicle" then return end
  npcID = tonumber(npcID)
  if not npcID then return end
  local name = UnitName(unit)
  if not name or isSecret(name) then return end
  local mapID = C_Map and C_Map.GetBestMapForUnit and C_Map.GetBestMapForUnit("player")
  local x, y
  if mapID and C_Map.GetPlayerMapPosition then
    local pos = C_Map.GetPlayerMapPosition(mapID, "player")
    if pos then x, y = pos:GetXY() end
  end
  DQNamesDB.npcs[npcID] = DQNamesDB.npcs[npcID] or name
  DQNamesDB.seen[npcID] = {
    name = name,
    zone = GetZoneText(),
    subzone = GetSubZoneText(),
    map = mapID,
    x = x and math.floor(x * 1000 + 0.5) / 10 or nil,
    y = y and math.floor(y * 1000 + 0.5) / 10 or nil,
  }
end

local function recordUnit(unit)
  pcall(recordUnitInner, unit)
end

---------------------------------------------------------------------------
-- 掃描流程：每 0.2 秒處理一批，沒拿到的放到下一輪，最多 6 輪
---------------------------------------------------------------------------
local queue, round, scanning = {}, 0, false
local done, total, lastTick = 0, 0, 0
local MAX_ROUNDS, BATCH = 6, 25

local function buildQueue()
  queue = {}
  for _, id in ipairs(DQNames_IDS.items) do if not DQNamesDB.items[id] then table.insert(queue, {"item", id}) end end
  for _, id in ipairs(DQNames_IDS.quests) do if not DQNamesDB.quests[id] then table.insert(queue, {"quest", id}) end end
  for _, id in ipairs(DQNames_IDS.npcs) do if not DQNamesDB.npcs[id] then table.insert(queue, {"npc", id}) end end
end

local function counts()
  local function n(t) local c = 0; for _ in pairs(t) do c = c + 1 end; return c end
  return n(DQNamesDB.items), #DQNames_IDS.items, n(DQNamesDB.quests), #DQNames_IDS.quests, n(DQNamesDB.npcs), #DQNames_IDS.npcs
end

local function status()
  local a, A, b, B, c, C = counts()
  say(("物品 %d/%d、任務 %d/%d、NPC %d/%d"):format(a, A, b, B, c, C))
end

local retry
local function step()
  if not scanning then return end
  for _ = 1, BATCH do
    local job = table.remove(queue, 1)
    if not job then break end
    local kind, id = job[1], job[2]
    local pok, ok = pcall(function()
      if kind == "item" then return tryItem(id) elseif kind == "quest" then return tryQuest(id) else return tryNpc(id) end
    end)
    if not (pok and ok) then table.insert(retry, job) end
    done = done + 1
  end
  if GetTime and GetTime() - lastTick > 5 then
    lastTick = GetTime()
    say(("進度：第 %d 輪，已處理 %d/%d"):format(round + 1, done, total))
  end
  if #queue > 0 then
    C_Timer.After(0.2, step)
  elseif #retry > 0 and round < MAX_ROUNDS then
    round = round + 1
    queue, retry = retry, {}
    done, total = 0, #queue
    say(("第 %d 輪補查，還有 %d 筆…"):format(round, #queue))
    C_Timer.After(2, step)
  else
    scanning = false
    status()
    if #retry > 0 then say(("有 %d 筆查不到，可能是遊戲尚未載入或不存在。NPC 可以在遊戲中選取它們來補上。"):format(#retry)) end
    say("掃描完成，請輸入 |cff4dff5e/reload|r 存檔。")
  end
end

local function startScan()
  if scanning then say(("正在掃描中：第 %d 輪，%d/%d。要重來請輸入 /dqscan stop"):format(round + 1, done, total)); return end
  buildQueue(); retry = {}; round = 0
  if #queue == 0 then say("全部都查過了。"); status(); return end
  scanning = true
  done, total, lastTick = 0, #queue, 0
  say(("開始掃描 %d 筆，請稍候約一兩分鐘…"):format(#queue))
  step()
end

SLASH_DQNAMES1 = "/dqscan"
SlashCmdList.DQNAMES = function(msg)
  msg = (msg or ""):lower()
  if msg == "status" then status(); if scanning then say(("掃描中：第 %d 輪，%d/%d"):format(round + 1, done, total)) end
  elseif msg == "stop" then scanning = false; say("已停止掃描。輸入 /reload 存檔。")
  elseif msg == "reset" then DQNamesDB = nil; initDB(); say("已清空掃描結果。")
  else startScan() end
end

f:RegisterEvent("ADDON_LOADED")
f:RegisterEvent("PLAYER_TARGET_CHANGED")
f:RegisterEvent("UPDATE_MOUSEOVER_UNIT")
f:SetScript("OnEvent", function(_, event, arg1)
  if event == "ADDON_LOADED" and arg1 == ADDON then
    initDB()
    say("已載入。輸入 |cff4dff5e/dqscan|r 開始掃描中文名稱。")
  elseif event == "PLAYER_TARGET_CHANGED" then
    if DQNamesDB then recordUnit("target") end
  elseif event == "UPDATE_MOUSEOVER_UNIT" then
    if DQNamesDB then recordUnit("mouseover") end
  end
end)

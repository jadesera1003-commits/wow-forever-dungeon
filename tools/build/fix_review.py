"""套用 data/quests/review_notes.md 的分類修正（可重複執行）。"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIX = [
 ('{d:"ubrs",c:"inside",n:"晉升印章",lv:60,xp:9950,npc:"裂盾滲透者",w:"副本內",note:"接在第一個「晉升印章」之後",side:"B",id:4743}',
  '{d:"ubrs",c:"skip",n:"晉升印章（第 2 步）",lv:60,xp:9950,npc:"裂盾滲透者",w:"副本內",reason:"目標在塵泥沼澤打艾博斯塔夫，不在副本內",side:"B",id:4743}'),
 ('note:"交給荒蕪之地・卡加斯的軍官高圖斯",side:"H",id:4903}',
  'note:"要殺下層的歐莫克、沃恩、維姆薩拉克，交給荒蕪之地・卡加斯的軍官高圖斯",side:"H",id:4903}'),
 ('{d:"brd",c:"direct",n:"卡蘭·巨錘",lv:59,xp:6400,npc:"國王麥格尼·銅鬚",w:"鐵爐堡 (39.4, 55.8)",tip:"到副本裡找卡蘭·巨錘對話",side:"A",id:4341}',
  '{d:"brd",c:"chain",n:"卡蘭·巨錘",lv:59,xp:6400,npc:"國王麥格尼·銅鬚",w:"鐵爐堡 (39.4, 55.8)",src:{q:"索瑞森廢墟",npc:"皇家歷史學家阿克瑟努斯",w:"鐵爐堡 (38.6, 55.4)",path:"索瑞森廢墟（燃燒平原蒐集聖物資訊）→ 本任務"},tip:"到副本裡找卡蘭·巨錘對話",side:"A",id:4341}'),
 ('{d:"sm-cath",c:"direct",n:"以聖光之名",npc:"虔誠的萊雷恩",w:"希爾斯布萊德丘陵 (51.4, 58.4)",lv:40,xp:4700,side:"A",id:1053}',
  '{d:"sm-cath",c:"chain",n:"以聖光之名",npc:"虔誠的萊雷恩",w:"希爾斯布萊德丘陵 (51.4, 58.4)",lv:40,xp:4700,src:{q:"血色之路",npc:"安東修士",w:"淒涼之地・尼耶爾前哨站 (66.4, 7.8)",path:"血色之路（把安東修士的表彰信交給南海鎮的萊雷恩）→ 本任務"},side:"A",id:1053}'),
 ('{d:"brs",c:"direct",n:"惡魔熔爐",lv:60,xp:8300,npc:"羅拉克斯",w:"冬泉谷 (63.8, 73.8)",side:"B",id:5127}',
  '{d:"brs",c:"chain",n:"惡魔熔爐",lv:60,xp:8300,npc:"羅拉克斯",w:"冬泉谷 (63.8, 73.8)",src:{q:"羅拉克斯的故事",npc:"羅拉克斯",w:"冬泉谷 (63.8, 73.8)",path:"先跟羅拉克斯對話聽故事 → 本任務"},note:"上層黑石塔殺古拉魯克，用血污長矛刺屍體",side:"B",id:5127}'),
 ('{d:"strat-ud",c:"direct",n:"吞嚥者拉姆斯登",lv:60,xp:6600,npc:"納薩諾斯·凋零者",w:"東瘟疫之地 (26.6, 74.8)",side:"H",id:6163}',
  '{d:"strat-ud",c:"chain",n:"吞嚥者拉姆斯登",lv:60,xp:6600,npc:"納薩諾斯·凋零者",w:"東瘟疫之地 (26.6, 74.8)",src:{q:"遊俠之王的命令",npc:"納薩諾斯·凋零者",w:"東瘟疫之地 (26.6, 74.8)",path:"遊俠之王的命令（奎爾林斯小屋）→ 暗翼蝠（瑪瑞斯農場北邊）→ 本任務"},side:"H",id:6163}'),
 ('{d:"st",c:"direct",n:"深入神廟",lv:51,xp:4900,npc:"瑪爾馮·瑞文斯克",w:"塔納利斯 (52.6, 45.8)",tip:"原版要先做「石環」，接不到的話先去做",side:"B",id:3446}',
  '{d:"st",c:"chain",n:"深入神廟",lv:51,xp:4900,npc:"瑪爾馮·瑞文斯克",w:"塔納利斯 (52.6, 45.8)",src:{q:"石環",npc:"瑪爾馮·瑞文斯克",w:"塔納利斯 (52.6, 45.8)",path:"石環（到棘齒城瑪爾馮的工坊拿石環）→ 本任務"},side:"B",id:3446}'),
 ('{d:"st",c:"direct",n:"雕像群的秘密",lv:51,xp:6100,npc:"瑪爾馮·瑞文斯克",w:"塔納利斯 (52.6, 45.8)",side:"B",id:3447}',
  '{d:"st",c:"chain",n:"雕像群的秘密",lv:51,xp:6100,npc:"瑪爾馮·瑞文斯克",w:"塔納利斯 (52.6, 45.8)",src:{q:"石環",npc:"瑪爾馮·瑞文斯克",w:"塔納利斯 (52.6, 45.8)",path:"石環（到棘齒城瑪爾馮的工坊拿石環）→ 本任務"},side:"B",id:3447}'),
 ('{d:"ubrs",c:"inside",n:"監護者",lv:60,xp:6600,npc:"奧比",w:"副本內",side:"B",id:5160}',
  '{d:"ubrs",c:"inside",n:"監護者",lv:60,xp:6600,npc:"奧比",w:"副本內",note:"副本內接，要到冬泉谷交給哈爾琳",side:"B",id:5160}'),
 ('w:"副本內・需要聖契物品",side:"B",id:7485}',
  'w:"副本內・需要聖契物品",note:"聯盟要先做「精靈的傳說」（找泰謬斯·尋夢者）才接得到",side:"B",id:7485}'),

 ('reason:"要先在副本裡做完哥沙克那幾步、回奧格瑪報告索爾，得再打一趟",side:"B",id:4003}', 'reason:"要先在副本裡做完哥沙克那幾步、回奧格瑪報告索爾，得再打一趟",side:"H",id:4003}'),
 ('reason:"救出公主之後的回報任務，接在「拯救公主」後面",side:"B",id:4004}', 'reason:"救出公主之後的回報任務，接在「拯救公主」後面",side:"H",id:4004}'),
]
for p in ['index.html', 'claude-artifact/index.html']:
    path = os.path.join(ROOT, p); h = open(path, encoding='utf-8').read(); n = 0
    for a, b in FIX:
        if a in h: h = h.replace(a, b); n += 1
    open(path, 'w', encoding='utf-8').write(h); print(p, 'fixed', n)

# 同一個副本裡名稱重複的任務：名稱後面補說明，避免混淆
import re
RENAME = {
 3982: '出了什麼事？（第 2 步：保護哥沙克）', 4001: '出了什麼事？（第 3 步：找卡蘭、回報索爾）',
 6521: '邪惡的盟友（交瑪克林大使的頭）', 6522: '邪惡的盟友（交小卷軸）',
 5463: '米奈希爾的禮物（在斯坦索姆放遺物）', 5464: '米奈希爾的禮物（交禁錮靈魂的遺物）',
 96376: '國家機密（奧格瑪接）', 96377: '國家機密（暴風城接）', 96379: '國家機密（荊棘谷接，兩陣營）',
}
for p in ['index.html', 'claude-artifact/index.html']:
    path = os.path.join(ROOT, p); lines = open(path, encoding='utf-8').read().split('\n'); n = 0
    for i, L in enumerate(lines):
        m = re.search(r',id:(\d+)[,}]', L)
        if L.startswith('  {d:') and m and int(m.group(1)) in RENAME:
            new = re.sub(r'([{,]n:")[^"]+(")', lambda mm: mm.group(1) + RENAME[int(m.group(1))] + mm.group(2), L, count=1)
            if new != L: lines[i] = new; n += 1
    open(path, 'w', encoding='utf-8').write('\n'.join(lines)); print(p, 'renamed', n)

# 「不共享」有兩種意思，分開寫清楚
WORD = [
 ('note:"採毒蛇花 ×10，不共享"', 'note:"採毒蛇花 ×10，每人要各自採（不共享）"'),
 ('note:"變異皮革 ×20，不共享"', 'note:"變異皮革 ×20，每人要各自撿（不共享）"'),
 ('note:"哀嚎香精 ×6，不共享"', 'note:"哀嚎香精 ×6，每人要各自撿（不共享）"'),
 ('reason:"碎裂的哨兵核心 ×6 不共享，五人隊要跑 2–3 趟"', 'reason:"碎裂的哨兵核心 ×6 每人要各自撿（不共享），五人隊要跑 2–3 趟"'),
 ('note:"學習石頭守護者看守的知識，不共享"', 'note:"學習石頭守護者看守的知識，每人要各自對話（進度不共享）"'),
 ('，進橘色區對地上的紅色小芽使用，不共享"', '，進橘色區對地上的紅色小芽使用，每人要各自做（進度不共享）"'),
 ('note:"接在「瑪拉頓的傳說」之後，不共享"', 'note:"接在「瑪拉頓的傳說」之後，每人要各自做（進度不共享）"'),
 ('note:"聯合墜飾＋靈魂墜飾，不共享"', 'note:"聯合墜飾＋靈魂墜飾，每人要各自撿（不共享）"'),
 ('note:"交給月光林地的守護者雷姆洛斯，不共享"', 'note:"交給月光林地的守護者雷姆洛斯，生命之種每人各自撿（不共享）"'),
 ('tip:"不可共享",side:"H",id:96376}', 'tip:"任務不能分享給隊友，每人自己去接",side:"H",id:96376}'),
 ('tip:"不可共享",side:"A",id:96377}', 'tip:"任務不能分享給隊友，每人自己去接",side:"A",id:96377}'),
 ('tip:"兩個陣營都能接，不可共享",side:"B",id:96379}', 'tip:"兩個陣營都能接；任務不能分享給隊友，每人自己去接",side:"B",id:96379}'),
]
for p in ['index.html', 'claude-artifact/index.html']:
    path = os.path.join(ROOT, p); h = open(path, encoding='utf-8').read(); n = 0
    for a, b in WORD:
        if a in h: h = h.replace(a, b); n += 1
    open(path, 'w', encoding='utf-8').write(h); print(p, 'share wording', n)

WORD2 = {'note:"採毒蛇花 ×10，每人要各自採（不共享）"': 'note:"採毒蛇花 ×10"', 'note:"變異皮革 ×20，每人要各自撿（不共享）"': 'note:"變異皮革 ×20"', 'note:"哀嚎香精 ×6，每人要各自撿（不共享）"': 'note:"哀嚎香精 ×6"', 'reason:"碎裂的哨兵核心 ×6 每人要各自撿（不共享），五人隊要跑 2–3 趟"': 'reason:"碎裂的哨兵核心 ×6 掉得少，五人隊要跑 2–3 趟才夠"', 'note:"學習石頭守護者看守的知識，每人要各自對話（進度不共享）"': 'note:"學習石頭守護者看守的知識"', '，進橘色區對地上的紅色小芽使用，每人要各自做（進度不共享）"': '，進橘色區對地上的紅色小芽使用"', 'note:"接在「瑪拉頓的傳說」之後，每人要各自做（進度不共享）"': 'note:"接在「瑪拉頓的傳說」之後"', 'note:"聯合墜飾＋靈魂墜飾，每人要各自撿（不共享）"': 'note:"聯合墜飾＋靈魂墜飾"', 'note:"交給月光林地的守護者雷姆洛斯，生命之種每人各自撿（不共享）"': 'note:"交給月光林地的守護者雷姆洛斯"', 'tip:"任務不能分享給隊友，每人自己去接",side:"H",id:96376}': 'side:"H",id:96376}', 'tip:"任務不能分享給隊友，每人自己去接",side:"A",id:96377}': 'side:"A",id:96377}', 'tip:"兩個陣營都能接；任務不能分享給隊友，每人自己去接",side:"B",id:96379}': 'tip:"兩個陣營都能接",side:"B",id:96379}'}
for p in ['index.html', 'claude-artifact/index.html']:
    path = os.path.join(ROOT, p); h = open(path, encoding='utf-8').read()
    for a, b in WORD2.items(): h = h.replace(a, b)
    open(path, 'w', encoding='utf-8').write(h)

# 依 Wowhead 區域任務清單（data/quests/zone_flags.json）補上職業／種族／陣營限制
PAL = ["聖騎士"]; HD = ["人類", "矮人"]
ATTR = {
 79946: {'cls': PAL, 'race': HD}, 79963: {'cls': PAL, 'race': HD}, 79970: {'cls': PAL, 'race': HD},
 84318: {'cls': PAL, 'race': HD}, 84319: {'cls': PAL, 'race': HD}, 84330: {'cls': PAL},
 7643: {'cls': PAL, 'race': HD}, 7644: {'cls': PAL, 'race': HD}, 7647: {'cls': PAL, 'race': HD},
 5127: {'cls': ["戰士", "聖騎士"]}, 5103: {'cls': ["戰士", "聖騎士", "薩滿"]}, 7463: {'cls': ["法師"]},
 8990: {'cls': ["戰士", "盜賊"]}, 8968: {'cls': ["獵人", "盜賊"]}, 7509: {'cls': ["戰士", "聖騎士"]},
 2951: {'side': "B"}, 95789: {'side': "B"},
 # 經典版 Wowhead 標「獸人、牛頭人、食人妖」，不死族不能接；Forever 頁面沒標，保留天裔精靈
 1049: {'race': ["獸人", "牛頭人", "食人妖", "天裔精靈"], 'tip': "不死族不能接（經典版限制，Wowhead Forever 頁面沒標示）"},
}
def setattr_line(L, key, val):
    js = json.dumps(val, ensure_ascii=False).replace(', ', ',') if not isinstance(val, str) else '"%s"' % val
    pat = re.compile(r',%s:(\[[^\]]*\]|"[^"]*")' % key)
    if pat.search(L): return pat.sub(',%s:%s' % (key, js), L, count=1)
    return re.sub(r',id:(\d+)', lambda m: ',%s:%s,id:%s' % (key, js, m.group(1)), L, count=1)
import json
for p in ['index.html', 'claude-artifact/index.html']:
    path = os.path.join(ROOT, p); lines = open(path, encoding='utf-8').read().split('\n'); n = 0
    for i, L in enumerate(lines):
        m = re.search(r',id:(\d+)[,}]', L)
        if L.startswith('  {d:') and m and int(m.group(1)) in ATTR:
            for k, v in ATTR[int(m.group(1))].items(): L = setattr_line(L, k, v)
            if L != lines[i]: lines[i] = L; n += 1
    open(path, 'w', encoding='utf-8').write('\n'.join(lines)); print(p, 'class/race/side', n)

# 羅德隆廢墟兩個前置：Wowhead 任務頁沒列「要求」，依玩家回報保留，補上中文名稱與 NPC
SRC2 = [
 ('src:{q:"A Recipe for Death（任務鏈）",npc:"NPC 待查",w:"Wowhead 尚未標出起點",warn:"Forever 正式上線後新增的前置，原本試算表寫可直接接"}',
  'src:{q:"致命配方（3 步）",npc:"藥劑師倫弗利爾",w:"提里斯法林地・布瑞爾",path:"致命配方 ×3（倫弗利爾 ↔ 幽暗城的大藥劑師法拉尼爾）→ 本任務",warn:"Wowhead 任務頁沒列這個前置，是玩家回報的"}'),
 ('src:{q:"Rear Guard Patrol（兩段）",npc:"NPC 待查",w:"提里斯法林地",path:"要先打掉提里斯法林地的 13 級精英 Riptear",warn:"Forever 正式上線後新增的前置，原本試算表寫可直接接"}',
  'src:{q:"巡查後方（2 步）",npc:"亡靈衛兵林奈",w:"提里斯法林地・布瑞爾",path:"巡查後方 → 巡查後方（第 2 步要打 13 級精英）→ 本任務",note2:"Wowhead 任務頁沒列這個前置，已在遊戲內確認需要"}'),
]
for p in ['index.html', 'claude-artifact/index.html']:
    path = os.path.join(ROOT, p); h = open(path, encoding='utf-8').read()
    for a, b in SRC2: h = h.replace(a, b)
    open(path, 'w', encoding='utf-8').write(h)

# 新的瘟疫：Wowhead 沒有任何前置，改回直接接（之前的「致命配方」前置查無出處）
NP_OLD = re.compile(r'\{d:"rfk-ruin",c:"chain",n:"新的瘟疫",.*?,id:95216\}')
NP_NEW = '{d:"rfk-ruin",c:"direct",n:"新的瘟疫",en:"The New Plague",npc:"薩多雷·格雷夫",w:"幽暗城・藥劑師區 (46.6, 71.4)",lv:16,xp:5450,note:"從首領枯萎之牙拿劇毒菌株",id:95216}'
for p in ['index.html', 'claude-artifact/index.html']:
    path = os.path.join(ROOT, p); h = open(path, encoding='utf-8').read()
    h = NP_OLD.sub(lambda m: NP_NEW, h)
    open(path, 'w', encoding='utf-8').write(h)

for p in ['index.html', 'claude-artifact/index.html']:
    path = os.path.join(ROOT, p); h = open(path, encoding='utf-8').read()
    h = h.replace('path:"巡查後方 → 巡查後方（第 2 步要打 13 級精英）→ 本任務",warn:"Wowhead 任務頁沒列這個前置，是玩家回報的"}', 'path:"巡查後方 → 巡查後方（第 2 步要打 13 級精英）→ 本任務",warn:"Wowhead 任務頁沒列這個前置，已在遊戲內確認需要"}')
    open(path, 'w', encoding='utf-8').write(h)

# 玩家在遊戲內確認需要前置（Wowhead 任務頁沒列）
CONFIRMED = [94968, 94972, 94975]
CW = '要先做完整條劇情系列才會開放（Wowhead 沒列，已在遊戲內確認）'
for p in ['index.html', 'claude-artifact/index.html']:
    path = os.path.join(ROOT, p); lines = open(path, encoding='utf-8').read().split('\n')
    for i, L in enumerate(lines):
        m = re.search(r',id:(\d+)[,}]', L)
        if not (L.startswith('  {d:') and m and int(m.group(1)) in CONFIRMED) or CW in L: continue
        L = L.replace(',warn:"Wowhead 任務頁沒列這個前置，已在遊戲內確認需要"', '')
        a = L.find('src:{'); d = 0
        for j in range(a + 4, len(L)):
            if L[j] == '{': d += 1
            elif L[j] == '}':
                d -= 1
                if d == 0: break
        seg = L[a:j]
        seg = re.sub(r',\s*"?warn"?:\s*"[^"]*"', '', seg)
        lines[i] = L[:a] + seg + ',warn:"' + CW + '"' + L[j:]
    open(path, 'w', encoding='utf-8').write('\n'.join(lines))

# 進副本前就能接、只是要多跑幾趟的收集任務：放回「直接接」，多趟寫在提示裡
TO_DIRECT = {
 3042: '{d:"zf",c:"direct",side:"B",n:"食人妖調和劑",en:"Troll Temper",npc:"特倫頓·輕錘",w:"塔納利斯・加基森 (51.4, 28.6)",lv:45,tip:"食人妖調和劑 ×20 掉率普通，玩家回報要打兩趟才收齊",id:3042}',
 95789: '{d:"drowned",c:"direct",side:"B",n:"被陰的鹽占海盜",en:"Shady Saltseers",npc:"克拉茲克",w:"荊棘谷・藏寶海灣 (27.0, 77.2)",lv:40,tip:"巫毒灌注神器 ×10 掉率很低，5 人一趟大約只拿到一半，通常要打兩趟",id:95789}',
 96988: '{d:"dalaran",c:"direct",side:"H",n:"力量的泉源",en:"Source of Power",npc:"馬丁·費爾本",w:"幽暗城 (46.6, 74.4)",lv:33,tip:"碎裂的哨兵核心 ×6 掉得少，五人隊要跑 2–3 趟才夠",id:96988}',
}
for p in ['index.html', 'claude-artifact/index.html']:
    path = os.path.join(ROOT, p); lines = open(path, encoding='utf-8').read().split('\n')
    for i, L in enumerate(lines):
        m = re.search(r',id:(\d+)[,}]', L)
        if L.startswith('  {d:') and m and int(m.group(1)) in TO_DIRECT and 'c:"skip"' in L:
            lines[i] = '  ' + TO_DIRECT[int(m.group(1))] + (',' if L.rstrip().endswith(',') else '')
    open(path, 'w', encoding='utf-8').write('\n'.join(lines))

# 深入血色修道院：拆到三個區各列一次（直接接），提示這區要殺誰
SM_OLD = '  {d:"sm-all",c:"skip",n:"深入血色修道院",en:"Into The Scarlet Monastery",reason:"要打圖書館、軍械庫、大教堂三個區，一趟做不完",id:1048},'
SM_BASE = 'c:"direct",n:"深入血色修道院",en:"Into The Scarlet Monastery",npc:"瓦里瑪薩斯",w:"幽暗城・皇家區 (56.2, 92.6)",lv:42,'
SM_NEW = '\n'.join([
 '  {d:"sm-lib",' + SM_BASE + 'tip:"要分三區做完：這區殺馴犬者洛克希；軍械庫殺赫洛德；大教堂殺莫格萊尼和懷特邁恩",id:1048},',
 '  {d:"sm-arm",' + SM_BASE + 'tip:"要分三區做完：這區殺赫洛德；圖書館殺馴犬者洛克希；大教堂殺莫格萊尼和懷特邁恩",id:1048},',
 '  {d:"sm-cath",' + SM_BASE + 'tip:"要分三區做完：這區殺莫格萊尼和懷特邁恩；圖書館殺馴犬者洛克希；軍械庫殺赫洛德",id:1048},'])
QS_OLD = 'reason:"鑄造奎爾塞拉第 2 步要奧妮克希亞的材料"'
QS_NEW = 'reason:"要到奧妮克希亞的巢穴（團隊副本）讓奧妮克希亞對劍噴火，不是五人副本的目標"'
for p in ['index.html', 'claude-artifact/index.html']:
    path = os.path.join(ROOT, p); h = open(path, encoding='utf-8').read()
    h = h.replace(SM_OLD, SM_NEW).replace(QS_OLD, QS_NEW)
    open(path, 'w', encoding='utf-8').write(h)

# 沉沒之城兩個任務的前置：Wowhead 玩家留言確認
DC = [
 ('src:{q:"暗礁海",npc:"肯維雷",w:"荊棘谷・格羅姆高 (32.2, 27.8)",path:"暗礁海 → 古拉巴什古代傳說 → 定位失落之城 → 本任務"}',
  'src:{q:"暗礁海",npc:"肯維雷",w:"荊棘谷・格羅姆高 (32.2, 27.8)",path:"暗礁海 → 古拉巴什古代傳說 → 定位失落之城 → 本任務",warn:"Wowhead 任務頁沒列，玩家留言確認要先做完這條"}'),
 ('src:{q:"暗礁海",npc:"肯維雷",w:"荊棘谷・格羅姆高 (32.2, 27.8)",path:"暗礁海 → … → 水中的敵人（指揮官阿格羅戈西）→ 本任務；也要先完成肯維雷的「定位失落之城」"}',
  'src:{q:"暗礁海",npc:"肯維雷",w:"荊棘谷・格羅姆高 (32.2, 27.8)",path:"暗礁海 → 古拉巴什古代傳說 → 水中的敵人（找指揮官阿格羅戈西接）→ 本任務；也要先做完肯維雷的「定位失落之城」",warn:"Wowhead 任務頁沒列，玩家留言確認。「水中的敵人」在水下打納迦收 10 把三叉戟，掉率低，建議先買水下呼吸藥水"}'),
]
for p in ['index.html', 'claude-artifact/index.html']:
    path = os.path.join(ROOT, p); h = open(path, encoding='utf-8').read()
    for a, b in DC: h = h.replace(a, b)
    open(path, 'w', encoding='utf-8').write(h)

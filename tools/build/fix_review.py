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

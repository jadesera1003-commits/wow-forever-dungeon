const BOSS_ORDER = {
  "wc":["安娜科德拉","考布萊恩","皮薩斯","克雷什","斯卡姆","瑟芬迪斯","永生者沃爾丹","吞噬者穆坦努斯","變異精靈龍","尖牙德魯伊"],
  "sfk":["雷希戈爾","席瓦萊恩男爵","指揮官斯普林瓦爾","屠夫拉佐克勞","盲眼守衛奧杜","吞噬者芬魯斯","狼王南杜斯","大法師阿魯高","阿魯高的虛空行者","地獄戰馬"],
  "bfd":["加摩拉","薩利維絲","格里哈斯特","洛古斯·傑特","阿奎尼斯男爵","夢遊者克爾里斯","瑟拉吉斯","阿庫麥爾"],
  "gnomer":["格魯比斯","粘性輻射塵","電刑器6000型","群體打擊者9-60","黑鐵大師","機電師瑟瑪普拉格"]
};
const SLOT = {1:"頭部",2:"頸部",3:"肩部",5:"胸部",20:"胸部",6:"腰部",7:"腿部",8:"腳",9:"手腕",10:"手",11:"手指",12:"飾品",13:"單手",14:"副手",15:"遠程",16:"背部",17:"雙手",21:"主手",22:"副手",23:"副手",25:"投擲",26:"遠程",28:"聖物"};
const WEAPON = {0:"斧",1:"雙手斧",2:"弓",3:"槍",4:"錘",5:"雙手錘",6:"長柄武器",7:"劍",8:"雙手劍",10:"法杖",13:"拳套",15:"匕首",16:"投擲武器",18:"弩",19:"魔杖",20:"魚竿"};
const ARMOR = {0:"其他",1:"布甲",2:"皮甲",3:"鎖甲",4:"鎧甲",6:"盾牌","-2":"戒指","-3":"項鍊","-4":"飾品","-5":"副手物品","-6":"背部"};
function itemType(cl, sc){
  if (cl === 2) return WEAPON[sc] || "武器";
  if (cl === 4) return ARMOR[sc] || "護甲";
  if (cl === 9) return "圖紙";
  if (cl === 12) return "任務物品";
  if (cl === 1) return "背包";
  return "其他";
}
/* 將 Wowhead 的 Forever 調整說明翻成中文 */
const CHG_WORDS = [["Item level","物品等級"],["Bonus armor","額外護甲"],["Armor","護甲"],["Strength","力量"],["Agility","敏捷"],["Stamina","耐力"],["Intellect","智力"],["Spirit","精神"],["Shadow Spell Power","暗影法術能量"],["Spell Power","法術能量"],["Spell Damage","法術傷害"],["Spell Penetration","法術穿透"],["Healing","治療"],["Attack Power","攻擊強度"],["Damage","傷害"],["Speed","速度"],["Durability","耐久"],["Health per 5 sec","每 5 秒生命"],["Mana per 5 sec","每 5 秒法力"],["Nature Resistance","自然抗性"],["Shadow Resistance","暗影抗性"],["Fire Resistance","火焰抗性"],["Frost Resistance","冰霜抗性"],["Arcane Resistance","秘法抗性"],["Defense","防禦"],["Binds when picked up","拾取後綁定"],["New icon","新圖示"],["Unique","唯一"],["Epic","史詩"],["Rare","精良"],["Uncommon","優秀"],["Common","普通"],["Mace (Main Hand)","主手錘"],["Mace (One-Hand)","單手錘"]];
function chgText(s){
  if (!s) return "";
  let t = s;
  t = t.replace(/\[\[([^\]]+)\] /g, "[$1 ");
  CHG_WORDS.forEach(([en, zh]) => { t = t.split(en).join(zh); });
  t = t.replace(/\[([^\[\]]*?) instead of ([^\[\]]*?)\]/g, "$1（原 $2）")
       .replace(/\[([^\[\]]*?) added\]/g, "新增 $1")
       .replace(/\[([^\[\]]*?) removed\]/g, "移除 $1")
       .replace(/\[([^\[\]]*?) changed\]/g, "$1有調整")
       .replace(/\[none\]/g, "無")
       .replace(/效果: .*?\]\]/g, "效果數值調整")
       .replace(/[\[\]]/g, "")
       .replace(/唯一 唯一/g, "唯一");
  return t.split(/(?<=）|調整|圖示|[0-9])\s+(?=[^\s（])/).join("・").replace(/\s{2,}/g, " ").trim();
}
function lootFor(id){
  if (LOOT[id]) return LOOT[id];
  const rows = RAW_LOOT[id];
  if (!rows) return null;
  const groups = {};
  rows.forEach(r => {
    const [iid, n, q, cl, sc, slot, req, src, chg] = r;
    const key = src === "-" ? "小怪／其他" : src.split("/")[0];
    (groups[key] = groups[key] || []).push({id:iid, n, q, slot: SLOT[slot] || (cl === 9 ? "圖紙" : cl === 12 ? "任務物品" : cl === 1 ? "背包" : "其他"), t: itemType(cl, sc), req, chg: chgText(chg), stats:[]});
  });
  const order = BOSS_ORDER[id] || [];
  const minReq = g => Math.min(...groups[g].map(i => i.req || 99));
  const names = Object.keys(groups).sort((a, b) => {
    if (a === "小怪／其他") return 1; if (b === "小怪／其他") return -1;
    const ia = order.indexOf(a), ib = order.indexOf(b);
    if (ia >= 0 && ib >= 0) return ia - ib;
    if (ia >= 0) return -1; if (ib >= 0) return 1;
    return minReq(a) - minReq(b);
  });
  return {note:"首領順序是大概的攻略順序，新副本依掉落等級排列。", bosses: names.map(n => ({n, lv:"", where: n === "小怪／其他" ? "副本內小怪或稀有怪" : "", quest:null, items: groups[n]}))};
}

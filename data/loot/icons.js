/* 自製部位圖示（線條 SVG，顏色跟著主題） */
const ICON = {
  "劍":'<path d="M18 3l3 3-9.5 9.5-3-3z"/><path d="M7 14l3 3M5 16l3 3M4 20l3-3"/>',
  "匕首":'<path d="M17 4l3 3-7 7-3-3z"/><path d="M8.5 12.5l3 3M6 16l2 2M4.5 19.5l2-2"/>',
  "錘":'<rect x="12" y="3" width="8" height="6" rx="1" transform="rotate(45 16 6)"/><path d="M12.5 11.5L4 20"/>',
  "拳套":'<path d="M7 10V7a2 2 0 014 0v3M11 9V6a2 2 0 014 0v4M15 10V8a2 2 0 014 0v5a7 7 0 01-7 7h-1a6 6 0 01-6-6v-2a2 2 0 014 0"/>',
  "弩":'<path d="M4 8c5 2 11 2 16 0M12 4v16M9 17l3 3 3-3"/><path d="M4 8l8 4 8-4"/>',
  "背部":'<path d="M8 4h8l3 16-7-3-7 3z"/><path d="M8 4c1 2 7 2 8 0"/>',
  "手腕":'<rect x="5" y="8" width="14" height="8" rx="3"/><path d="M9 8v8M15 8v8"/>',
  "胸部":'<path d="M8 4l4 2 4-2 4 4-2 3v9H6v-9L4 8z"/><path d="M12 6v14"/>',
  "腳":'<path d="M8 3h5v10l6 3v4H5v-4l3-2z"/><path d="M5 18h14"/>',
  "頭部":'<path d="M5 14a7 7 0 0114 0v3H5z"/><path d="M9 17v3M15 17v3M8 11h8"/>',
  "肩部":'<path d="M3 15c0-5 4-8 9-8s9 3 9 8"/><path d="M3 15h6l3-3 3 3h6"/>',
  "腰部":'<rect x="3" y="9" width="18" height="6" rx="2"/><rect x="10" y="8" width="4" height="8" rx="1"/>',
  "腿部":'<path d="M7 3h10l-1 18h-3l-1-11-1 11H8z"/>',
  "手":'<path d="M8 21v-6l-3-4 2-1 3 3V5a1.5 1.5 0 013 0v6M13 11V4a1.5 1.5 0 013 0v7M16 11V6a1.5 1.5 0 013 0v9a6 6 0 01-6 6H8"/>',
  "戒指":'<circle cx="12" cy="14" r="6"/><path d="M9 6l3-3 3 3-3 2z"/>',
  "項鍊":'<path d="M5 4c0 6 3 9 7 9s7-3 7-9"/><path d="M12 13l-2 3 2 4 2-4z"/>',
  "飾品":'<path d="M12 3l2.5 5.5L20 9l-4 4 1 6-5-3-5 3 1-6-4-4 5.5-.5z"/>',
  "盾牌":'<path d="M12 3l8 3v6c0 5-4 8-8 9-4-1-8-4-8-9V6z"/><path d="M12 3v18"/>',
  "副手物品":'<path d="M9 3h6l-1 4h-4z"/><path d="M8 7h8l2 14H6z"/>',
  "法杖":'<path d="M6 21L17 7"/><circle cx="18" cy="6" r="2.5"/><path d="M15 4l1 1M20 9l1 1"/>',
  "魔杖":'<path d="M5 19L15 9"/><path d="M17 3l1 2 2 1-2 1-1 2-1-2-2-1 2-1z"/>',
  "斧":'<path d="M6 21L18 5"/><path d="M13 5c3-2 7 0 7 4l-4 1z"/>',
  "雙手斧":'<path d="M5 21L19 5"/><path d="M13 5c3-2 7 0 7 4l-4 1zM11 9c-3 2-3 6 0 8l2-4z"/>',
  "雙手劍":'<path d="M19 3l2 2L9 17l-2-2z"/><path d="M5 13l6 6M4 20l3-3"/>',
  "雙手錘":'<rect x="11" y="2" width="9" height="7" rx="1" transform="rotate(45 15.5 5.5)"/><path d="M12 12L3 21"/>',
  "弓":'<path d="M6 3c8 3 8 15 0 18"/><path d="M6 3v18M4 12h14M15 9l3 3-3 3"/>',
  "槍":'<path d="M3 10h14l3-2v4l-3 1H9l-2 6H4l1-6H3z"/>',
  "長柄武器":'<path d="M5 21L17 7"/><path d="M15 3l6 6-3 1-4-4z"/>',
  "投擲武器":'<path d="M6 21L18 5"/><path d="M13 5c3-2 7 0 7 4l-4 1z"/><path d="M3 15l3-1M4 19l3-2"/>',
  "圖紙":'<path d="M5 3h10l4 4v14H5z"/><path d="M15 3v4h4M8 12h8M8 16h6"/>',
  "任務物品":'<circle cx="12" cy="12" r="8"/><path d="M12 7v6M12 16v.5"/>',
  "背包":'<path d="M6 8h12l1 13H5z"/><path d="M9 8a3 3 0 016 0"/>'
};
const ARMOR_SLOT_ICON = {"布甲":1,"皮甲":1,"鎖甲":1,"鎧甲":1};
function iconFor(it){
  let k = ARMOR_SLOT_ICON[it.t] ? it.slot : it.t;
  if (!ICON[k]) k = ICON[it.slot] ? it.slot : "飾品";
  return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICON[k] + '</svg>';
}

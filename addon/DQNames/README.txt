DQNames 安裝與使用說明
=====================

一、安裝
1. 找到 Forever 的遊戲資料夾，例如：
   C:\Program Files (x86)\World of Warcraft\_forever_\
   （資料夾名稱以你電腦上實際看到的為準）
2. 把整個「DQNames」資料夾放進：
   ...\_forever_\Interface\AddOns\
   放好後路徑應該是 ...\Interface\AddOns\DQNames\DQNames.toc
3. 進遊戲前在角色選擇畫面點左下角「插件」，確認 DQNames 有勾選。
   如果顯示「過期」，勾選上方的「載入過期插件」。

二、使用
1. 登入任一角色後，聊天框會出現「[DQNames] 已載入」。
2. 輸入 /dqscan 開始掃描，約一兩分鐘。
3. 看到「掃描完成」後，輸入 /reload 存檔（一定要做，不然資料不會寫進檔案）。
4. 其他指令：
   /dqscan status  看目前進度
   /dqscan reset   清空重來

三、平常玩的時候
插件會在你選取或滑鼠移過 NPC 時，自動記下它的中文名稱和所在位置。
這些資料也會在登出或 /reload 時存檔。

四、把結果交給 Claude
掃描結果存在：
...\_forever_\WTF\Account\你的帳號名稱\SavedVariables\DQNames.lua
把這個檔案傳給 Claude，或在 Claude 桌面 App 授權這個資料夾讓 Claude 直接讀取。

五、第一次使用請回報
1. 在遊戲輸入：/run print((select(4, GetBuildInfo())))
   把顯示的數字告訴 Claude，用來更新 DQNames.toc 第一行的版本號。
2. 如果掃描時跳出錯誤訊息，把訊息內容貼給 Claude。

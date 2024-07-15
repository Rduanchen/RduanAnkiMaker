# RduanAnkiMaker 
> V.1.0.0
![alt text](https://raw.githubusercontent.com/Rduanchen/RduanAnkiMaker/main/image.png)


## 簡介
RduanAnkiMaker 是一個用來製作 Anki 卡片的工具，安裝完之後，只需要輸入您想輸入的音文字母，就可以自動製作含有英文定義、翻譯、造句、音訊等資料的 Anki txt 檔案，您只需要將其匯入到Anki即可

## 安裝以及啟動
>需要的指令如下
### 下載exe檔案

exe 檔案會自動顯示在release 的地方(往您的右邊看就會看到)

mac 的朋友請到以下的網址下載
https://web.rduansharingpoint.site/RduanAnki/App

### 下載python專案
```
pip install -r requirements.txt
```
```
python App.py
```


此時您的終端機應該會有一段ip，請將其複製到瀏覽器中，然後按下Enter，即可進入到RduanAnkiMaker的主頁面，例如: http://127.0.0.1:5990/

此專案的預設網址為: http://127.0.0.1:5990/


## 使用方法

1. 在網頁打開的時候，請先按下右上角的設定按鈕，以確保設定皆為正確
2. 在左側的文字框先輸入單字，並且按下送出
3. 等待翻譯資料回傳的時候，您可以透過文字框修改您的卡片資料
4. 依照個人的需求，點擊需要下載的音訊檔案、文字檔
5. 此時您需要將`zip` 先解壓縮，再將裡面所有的音訊檔複製到Anki 的媒體資料夾，以下官方的說明文件將會教您如何找到您的Anki資料夾，您必須進入到使用者資料夾(應該叫`使用者1`之類的)，進入之後選擇`collection.media`的資料夾，將音訊檔案複製進去即可，例如:`user1/collection.media/`

以下資訊來自Anki官網:
https://docs.ankiweb.net/files.html

On Windows, the latest Anki versions store your Anki files in your appdata folder. You can access it by opening the file manager, and typing %APPDATA%\Anki2 in the location field. Older versions of Anki stored your Anki files in a folder called Anki in your Documents folder.

On Mac computers, recent Anki versions store all their files in the ~/Library/Application Support/Anki2 folder. The Library folder is hidden by default, but can be revealed in Finder by holding down the option key while clicking on the Go menu. If you're on an older Anki version, your Anki files will be in your Documents/Anki folder.

On Linux, recent Anki versions store your data in ~/.local/share/Anki2, or $XDG_DATA_HOME/Anki2 if you have set a custom data path. Older versions of Anki stored your files in ~/Documents/Anki or ~/Anki.



## 匯入Anki
在匯入Anki 的時候，一定要將 "允許html"的功能打開，才能使卡片被正確渲染
如果您不知道怎麼樣加入anki卡片中，請看以下的官方文件:
https://docs.ankiweb.net/templates/styling.html



# 注意事項
1. 本作者僅是在此紀錄程式碼，如果您取用之後，本作者並不負任何法律責任
2. 本專案採MIT授權，即便如此希望您不要將此專案用於商業用途
3. 歡迎各方高手一同精進此程式的功能
   

# Todo
* ~~Windows 的exe檔~~ (Solved)
* Mac 的exe檔
* KK 音標
* 下載音檔會出現的bug

# 版本歷程
* 0.1.0
  * 第一個版本
  * 含有基本輸出卡片功能
* 0.1.1
  * 修改了一些錯誤
  * 自動打開瀏覽器
* 0.2.0
  * 修復了媒體下載的問題
  * 可以打包成exe的檔案
* 0.3.0
  * 使用了多執行緒增進翻譯速度
  * 修復了一些錯誤
* 1.0.0
  * 增加了kk音標
  * 增加了單字的刪除按鈕
  * 介面大優化
  * 允許使用者自行調整輸入來源
  * 允許使用者編輯卡片資料

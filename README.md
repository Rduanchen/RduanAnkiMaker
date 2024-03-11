# RduanAnkiMaker 
> V.0.1.1
![alt text](https://raw.githubusercontent.com/Rduanchen/RduanAnkiMaker/main/image.png)

## Hotproblem
1. 刪除單字的按鈕有問題
2. 音訊檔案的命名格式不正確

## 簡介
RduanAnkiMaker 是一個用來製作 Anki 卡片的工具，安裝完之後，只需要輸入您想輸入的音文字母，就可以自動製作含有英文定義、翻譯、造句、音訊等資料的 Anki txt 檔案，您只需要將其匯入到Anki即可

## 安裝以及啟動
>需要的指令如下
### 下載exe檔案
**在本專案中的exe直接下載即可使用，exe 仍停留在0.2.0版本，如果您想要使用最新的版本，請下載python專案並啟動，本人會盡快更新exe檔案。**

**新版的Thread核心仍在測試中，如欲使用請執行lighter.py的檔案**


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
1. 在主頁面中輸入您想要查詢的單字，一次可以輸入多個單字
2. 按下查詢按鈕即可
3. 因為程式會自動去查詢單字的音訊，所以可能會需要一點時間
4. 顯示找尋結果之後，您可以選擇是否要匯入到anki，如果您選擇匯入到anki那麼請運閱讀以下的說明

## 製作卡片種類
1. 製作卡片有兩種選項，一種是含有音訊檔，另外一種是沒有音訊檔，如果您選擇「製作純文字檔｣，那麼你瀏覽器會直接下載文字檔，您可以跳過以下的步驟，直接到「匯入Anki的段落」
2. 如果您選擇了下載音訊檔案的選項，那麼您會多兩個選項，一個是下載文字檔，另一個是下載音訊檔，請您兩個按鈕都點擊，網頁會下載兩個檔案，一個是`.txt` 檔案，一個是`zip`檔案，
3. 此時您需要將`zip` 先解壓縮，再將裡面所有的音訊檔複製到Anki 的媒體資料夾，以下官方的說明文件將會教您如何找到您的Anki資料夾，您必須進入到使用者資料夾(應該叫`使用者1`之類的)，進入之後選擇`collection.media`的資料夾，將音訊檔案複製進去即可，例如:`user1/collection.media/`

以下資訊來自Anki官網:
https://docs.ankiweb.net/files.html

On Windows, the latest Anki versions store your Anki files in your appdata folder. You can access it by opening the file manager, and typing %APPDATA%\Anki2 in the location field. Older versions of Anki stored your Anki files in a folder called Anki in your Documents folder.

On Mac computers, recent Anki versions store all their files in the ~/Library/Application Support/Anki2 folder. The Library folder is hidden by default, but can be revealed in Finder by holding down the option key while clicking on the Go menu. If you're on an older Anki version, your Anki files will be in your Documents/Anki folder.

On Linux, recent Anki versions store your data in ~/.local/share/Anki2, or $XDG_DATA_HOME/Anki2 if you have set a custom data path. Older versions of Anki stored your files in ~/Documents/Anki or ~/Anki.



## 匯入Anki
1. 在匯入Anki 的時候，一定要將 "允許html"的功能打開，才能使卡片被正確渲染
2. 本專案有提供一個卡片靠左對齊的樣式可以選擇，如下:
```
.card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
		 display: flex;
		 flex-direction: column;
	  justify-content: center;
}
.RduanCard{
	display: flex;
	flex-direction: column;
	justify-content: flex-start;
	text-align: start;
	align-items: flex-start;
}
```
至於怎麼樣加入anki卡片中，請看以下的官方文件:
https://docs.ankiweb.net/templates/styling.html



# 注意事項
1. 本作者僅是在此紀錄程式碼，如果您取用之後，本作者並不負任何法律責任
2. 本專案採MIT授權，即便如此希望您不要將此專案用於商業用途
3. 歡迎各方高手一同精進此程式的功能
   

# Todo
1. 支援kk音標
2. 支援更多輸入方式
3. 支援更多卡片樣式
4. 支援macOS exe打包
5. 調整輸出方式

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

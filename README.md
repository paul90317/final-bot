# TOC Project 2020  
**伺服器測試機器人**  
Line ID: @866jaryx  
QR code:  
![qrc](imgs/qrc.png)  
[heroku FSM](https://asd4f5a.herokuapp.com/)  
## 啟發
這個機器人的主題是 **小工具**，主要是因為，當我們使用自己寫的 server 使用到 GET 以外的 HTTP Request method (像是 POST) 可能比較難 debug，所以我這裡提供一種方法，讓我們能使用聊天機器人幫你測試(類似 postman)。  

## 構想
首先這次作業規定使用 FSM,相信是為了符合計算理論的主題，根據 [維基百科](https://zh.wikipedia.org/wiki/%E6%9C%89%E9%99%90%E7%8A%B6%E6%80%81%E6%9C%BA) 的定義(如圖)，  
![FSM 邏輯圖](https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Finite_State_Machine_Logic.svg/800px-Finite_State_Machine_Logic.svg.png)  
我們只能使用上一狀態的 input，產生 output，這代表如果我們把 網址 當 input ,method 當 state，就沒地方放request header, body等等的東西了，但好在這個 linebot 只是要簡單 debug。  
因為 heroku 不知為何無法安裝 `transitions`，所以自己做(山不轉路轉)，好在 python 有類似 function pointer 的功能，做起來部會太難。  
## FSM
因為開發(本地)環境沒問題，所以圖是用 `GraphMachine` 畫的  
![FSM](/fsm.png)  
> 如果下一 state 只有 else transition 會再跳下一個 state，類似 lambda transition
## 實際測試
我們先測試 post 請求  
![p1](imgs/post/1.png)  
![p2](imgs/post/2.png)  
![p3](imgs/post/3.png)  
點擊 "立即查看"  
![res](imgs/post/res.png)  
如果是用 GET method，只會拿到 fsm.png，也就是說如果你只是把網址打到瀏覽器，根本無法測試 POST method，而本 linebot 很好的解決此問題。  
**抓 youtube**  
![3](imgs/3.png)  
![4](imgs/4.png)  
網址有被重新導向過  
**抓 facebook**  
![5](imgs/5.png)  

* 可以看到有些地方沒有畫面，是因為爬蟲沒辦法抓 local dependence(像 css 檔，抓到的檔案 fetch 也沒辦法用)。  
* facebook 顯示登入畫面是因為爬蟲就像是沒有登入的使用者，除非有給 header。  

## 難點克服
1. **傳送檔案太大**  
我的程式主要是用來測試，所以爬蟲抓到的資料希望可以完整地交給 client，但訊息大小有上限，所以使用 [firebase realtime database](db.py) 存放抓到的檔案，不同 user 根據 uid 有不同的 path ，那些就是他們的暫存區，當機器成功抓好網頁後會有超連結可以查看抓到甚麼。    
**超連結格式:** `https://[linebot 所在域名]/temp/[sha256 user's uid].html`  
![1](imgs/1.png)  
2. **heroku 無法安裝 graphviz**  
另外我的圖是 [draw.py](draw.py) 畫出來的，因為 heroku 似乎沒辦法安裝 graphviz 就算用了去年的方法，[環境](./Pipfile) 要分一下 ，dev-packages 是可畫圖的，而 packages 是推 heroku，而我的狀態機是採用 [構想](#構想) 的方法，寫在 [fsm.py](fsm.py) 裡  
## 功能展示
以下是主畫面  
![6](imgs/6.png)  
查詢機器人經過的 IP  
![7](imgs/7.png)  
測試伺服器，輸入請求  
![8](imgs/8.png)  
![9](imgs/9.png)  
regular expression 擋掉非法網址(ex. 域名有 + 號)  
![10](imgs/10.png)  
輸入翻譯的網站當測試  
![11](imgs/11.png)  
![1](imgs/1.png)  
點 立刻查看，網頁被存到機器人所在伺服器域名的 temp path 內。  
![12](imgs/12.png)  
## regular expression  
對於 http, https 網址  
`'https?:\/\/[a-zA-Z0-9\-]+(\.[a-zA-Z0-9]+)*(\/\S*)?'`  
我自己規定的，所以比較寬鬆。  
將 regular expression 分成三部份看，
`'https?:\/\/`, `[a-zA-Z0-9\-]+(\.[a-zA-Z0-9]+)*`, `(\/\S*)?'`  
第一部分代表 `http(s)://`，`s?` 代表 s 可有可無  
第二部分表示域名，大小寫數字皆有(我規定的)，子域名一定要有，子域名接受 `-`，  
第三部分代表 path, `/` 可有可無，`/` 後 path `\S` 接受所有字元。  
## 同時服務多個 client
每個 client 有各自的 uid，以 uid 的 sha256 當 key，用 [firebase realtime database](db.py) 儲存使用者的 state，實現多使用者同時與 linebot 聊天，state 不衝突。  
由於使用了 database，所以狀態不會因 heroku 睡著而消失。  
## database and deploy
![database](imgs/database.png)  
* 使用 heroku 當 server  
HOST_URL= https://asd4f5a.herokuapp.com/  
* 使用 firebase realtime database 當 database  
DB_URL= [readtime database -> 資料 -> 底下圖片上面的網址]  
![data](imgs/data.png)
## how to deploy  
基本上 clone 下來就可以 deploy 了，但要先設定 heroku 環境變數，如下:  
![var](imgs/var.png)  
DB_KEY 是 firebase 私密金鑰，取得方式是  
先進專案->設定圖標->專案設定->服務帳戶->產生新的私密金鑰  
檔案裡的內容就是了

## how to build local
**Step 1: clone 與環境變數**  
環境: window10 wsl python3.6  
首先開一個 wsl terrminal，然後輸入以下命令  
```wsl
git clone git@github.com:paul90317/final-bot.git
cd final-bot
vim .env
```
開始編輯環境變數，有哪些變數?
```env
LINE_CHANNEL_SECRET=...
LINE_CHANNEL_ACCESS_TOKEN=...
HOST_URL=...
DB_KEY=...
DB_URL=...
```
LINE_CHANNEL_SECRET 在你的 line platform 的 console 裡點擊 [Basic settings] -> [Channel secret]。  
LINE_CHANNEL_ACCESS_TOKEN 在 [Messaging API] -> [Channel access token]。  
HOST_URL 請輸入你的 Server 的跟路徑，待會會提到。  
DB_KEY, DB_URL 去 firebase 建立自己的 realtime database，詳情看 [前一段](## how to deploy)。  
  
**Step 2: Line Platform**  
用好後記得將 "[HOST_URL]/callback" 輸入 [Messaging API] -> [Webhook URL]。  
  
**Step 3: pipenv**  
python version: 3.6  
編輯完 .env 後，繼續輸入以下命令。  
```wsl
pipenv check
pipenv install --dev
pipenv shell
```
python 環境建立完成  
  
**Step 4: 畫 FSM 圖**  
```wsl
python draw.py
```
檔案輸出在 [fsm.png](./fsm.png)  
  
**Step 5: 啟動 server**  
輸入以下命令  
```wsl
python app.py
```
接者你會看到他監聽哪個 port(通常 5000)。  
接著再打開另一個終端機輸入  
```wsl
ngrok http 5000
```
該命令會在你 5000 打開一個公共開口，讓 line plat form 可以找到你的 server。  
你應該會看到 Forwarding 有個 https 網址，該網址就是 HOST_URL，用這個 HOST_URL 去完成 **Step 2, 3**，網路通了，就能加該機器人好友，開始聊天。  
## Grading
**Basic**  
* Able to show or generate FSM Diagram  
* Bot running properly  
* At least 3 states for FSM  
  
**Functionality**  
1. State complexity (對於輸入網址的處裡)  
2. CRU (database 暫存爬蟲抓取的結果、user state))  
3. Parsing (網址的 regular expression)  
  
**Creativity**  
* Tools(類似 postman 的網站測試工具)    
  
**Bonus**  
* Deploy  
1. image  
2. web crawling (測試網站、查詢 IP)  
3. binding database (firebase realtime database)  
4. others (再傳送網址時有特別將 uid hash)
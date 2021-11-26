# WTMS 自動打卡

### Change Log
* Build: flyhead/wtms:2021.0.1
> 1. Create WTMS based on Docker solution
> 2. Use Advance Python Scheduler for scheduling  
> 3. Use Chrome Server on port 4444 for headless simulation   
> 4. Add Clock job 

* Build: flyhead/wtms:2021.0.2
> 1. use Flask server for interworking on port 5000
> 2. Add API for overview
> 3. Add API for clock now
> 4. Add API for viewiong PNG files under screenshot folder 
> 5. Add API for approval of reclock requests

## 快速安裝
### 所需環境 

* 安裝 WSL2， 安裝說明: https://docs.microsoft.com/zh-tw/windows/wsl/install-win10
* 安裝 Docker Desktop for Windows，安裝說明: https://docs.docker.com/docker-for-windows/install/
(在Docker Desktop安裝後可略過Tutorial)

### 安裝步驟
* 建立新目錄 RPA
```shell
cd C:\Users\<USER_NAME>\AppData\Local
mkdir RPA
```

* 下載部屬檔 https://github.com/flyhead30042/RPA/blob/master/docker-compose.yml 至 RPA 目錄下
* 建立環境變數檔 .env，
* 複製下列內容至 .env 中

```commandline
WTMS_URL=https://working-time-management-system-tw.internal.ericsson.com/#/login
WTMS_ID=your_login_id (記得要修改)
WTMS_PWD=your_login_password (記得要修改)
CLOCK_ON_TIME=09:30
CLOCK_OUT_TIME=18:30
CRONTAB_CLOCK="15 13 * * mon-fri"
LOG_LEVEL=INFO
```  

* 切換到 RPA 目錄下
```commandline
cd C:\Users\<USER_NAME>\AppData\local\RPA
```

執行下列指令先移除舊 container，
```commandline
docker-compose -f .\docker-compose.yml down
```

* 執行下列指令進行部屬，第一次執行需下載 image ，會需要較久的時間
```commandline
docker-compose -f .\docker-compose.yml up -d chrome
docker-compose -f .\docker-compose.yml up -d wtms
```

* 執行下面指令，讓 docker engine 重開後也會自動把 container 帶起來
```commandline
docker update --restart unless-stopped rpa_chrome_1 
docker update --restart unless-stopped rpa_wtms_1
```

* 執行下列指令確定 selenium/standalone-chrome 和 flyhead/wtms 兩個 images 正確下載，記得要確認 Tag 中的版本編號為最新的版本 
```commandline
docker-compose images
```

```shell
Container           Repository                   Tag                 Image Id            Size
rpa_chrome_1        selenium/standalone-chrome   latest              c59dc2754f9f        1.05GB
rpa_wtms_1          flyhead/wtms                 2021.0.1            2e089bfe0d47        127MB
```

* 執行下列指令確定 container 正確執行 
```commandline
docker-compose ps
```
```shell
NAME                COMMAND                  SERVICE             STATUS              PORTS
rpa_chrome_1        "/opt/bin/entry_poin…"   chrome              running             0.0.0.0:4444->4444/tcp, :::4444->4444/tcp
rpa_wtms_1          "python /usr/local/s…"   wtms                running
```


## 系統參數說明
* WTMS_URL: WTMS 網址
* WTMS_ID: 登入 WTMS 帳號
* WTMS_PWD: 登入 WTMS 密碼
* CLOCK_ON_TIME: 打卡上班的時間，格式 hh:mm ，ex. 09:30
* CLOCK_OUT_TIME: 打卡下班的時間，格式 hh:mm ，ex. 18:45
* CRONTAB_CLOCK：打卡系統啟動時間，格式比照 crontab， mm hh DD MM Day of Week， 
ex. 15 13 * * mon-fri 代表周一到周五每天 13:15 會執行， */15 18 * * * 代表每天六點開始，每隔15分鐘執行，最後記得要用雙引號括起來
* LOG_LEVEL: logging 等級，支援 DEBUG, INFO, ERROR

## WTMS  指令
* Overview: List all infomration of WTMS including parameters, status and availabe API etc
```commandline
http://localhost:5000/wtms
```
* Clock Now: Clock immediately
```commandline
http://localhost:5000/wtms/clock
```
* View Screenshot: List all files under screenshot folder with name and timestamp attached
```commandline
http://localhost:5000/wtms/screenshot
```
* Approve Reclock Now: Approve all reclock requests immediately. ** Note it requires the authorization setting on TWMS **	
```commandline
http://localhost:5000/wtms/approve
```
## 常用 Docker 指令
* 看 wtms service 最後20行 log
```commandline
docket-compose logs wtms --tails=20
```
* 暫停並移除 container 
```commandline
docket-compose down
```

* 查詢使用的 image 
```commandline
docket-compose images
```

* 查詢使用的 container 狀況
```commandline
docket-compose ps
```

## Q&A
 * 兩種方式可以確定執行狀況
 * 1) 檢查 log 
 ```
 docker-compose logs  wtms  --tail=20  
 
wtms_1  | 2021-08-12 13:15:00,015 | apscheduler.executors.default | INFO | Running job "main (trigger: cron[month='*', day='*', day_of_week='mon-fri', hour='13', minute='15'], next run at: 2021-08-13 13:15:00 CST)" (scheduled at 2021-08-12 13:15:00+08:00)
wtms_1  | 2021-08-12 13:15:00,325 | clock | INFO | 1. Open https://working-time-management-system-tw.internal.ericsson.com/#/login
wtms_1  | 2021-08-12 13:15:07,901 | clock | INFO | 2. login with credentials
wtms_1  | 2021-08-12 13:15:11,397 | clock | INFO | 3. Clock On at 09:30
wtms_1  | 2021-08-12 13:15:22,748 | clock | INFO | 4. Clock Out at 18:30
wtms_1  | 2021-08-12 13:15:26,174 | apscheduler.executors.default | INFO | Job "main (trigger: cron[month='*', day='*', day_of_week='mon-fri', hour='13', minute='15'], next run at: 2021-08-13 13:15:00 CST)" executed successfully
 ```
 * 2) C:\Users\<USER_NAME>\AppData\local\RPA\wtms\screenshot 下有四個螢幕截圖，代表開啟網站(open.png)，登入(login.png)，clock in (clock_in.png)和 clock out(clock_out.png)。系統會覆蓋之前的截圖，所以永遠只有四張最新的截圖。
 
 * 除了上述的方式，也可以到右下角 tray 中，右鍵點選小鯨魚，選擇 "Dashboard"，"Containers/Apps"，就可以看見執行中的 Containers: rpa_chrome_1 和 rpa_wtms_1，顏色應該是淺藍色，如果是橘色或灰色則代表有錯誤發生了
 * 點選 container，可以看到 container 的 輸出 log
 * 如果有需要重啟系統，請參考 "執行下列指令開始部屬...." 開始的指令重跑一次就可以了

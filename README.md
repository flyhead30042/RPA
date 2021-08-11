# WTMS 自動打卡

## 快速安裝
### 所需環境 

* 安裝 WSL2， 安裝說明: https://docs.microsoft.com/zh-tw/windows/wsl/install-win10
* 安裝 Docker Desktop for Windows，安裝說明: https://docs.docker.com/docker-for-windows/install/
(在Docker Desktop安裝後可略過Tutorial)

### 安裝步驟
* 建立新目錄 RPA
```shell
cd C:\Users\<USER_NAME>\AppData\local
mkdir RPA
```

* 下載 https://github.com/flyhead30042/RPA/blob/master/docker-compose.yml 至 RPA 目錄下
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
* 執行下列指令開始部屬 ，第一次執行需下載 image ，會需要較久的時間
```commandline
docker-compose -f .\docker-compose.yml up -d chrome
docker-compose -f .\docker-compose.yml up -d wtms
```

* 執行下列指令確定 selenium/standalone-chrome 和 flyhead/wtms 兩個 images 正確下載 
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

## 常用指令
* 看 log
```commandline
docket-compose logs
```
* 暫停並移除 container 
```commandline
docket-compose down
```

* 查詢使用的 image 
```commandline
docket-compose images
```

* 查詢使用的 container 
```commandline
docket-compose ps
```

## Troubleshooting
 * TBC
# 快速安裝
## 所需環境 
* 在 Windows 10 下使用 WSL 2  建立 Docker 執行環境 
* WSL2 安裝說明: https://docs.microsoft.com/zh-tw/windows/wsl/install-win10

## 安裝步驟
* cd C:\Users\<USER_NAME>\AppData\local
* 建立新目錄 RPA 
* 下載 https://github.com/flyhead30042/RPA/blob/master/docker-compose.yml 至 RPA 目錄下
* 建立環境變數檔 .env，
* 複製下列內容至 .env 中

```buildoutcfg
WTMS_URL=https://working-time-management-system-tw.internal.ericsson.com/#/login
WTMS_ID=your_login_id (記得要修改)
WTMS_PWD=your_login_password (記得要修改)
CLOCK_ON_TIME=09:30
CLOCK_OUT_TIME=18:30
CRONTAB_CLOCK="15 13 * * mon-fri"
LOG_LEVEL=INFO
```  


* cd C:\Users\<USER_NAME>\AppData\local\RPA
* 執行下列指令 ，因為下載 image ，第一次會較久
```commandline
docker-compose -f .\docker-compose.yml up -d chrome
docker-compose -f .\docker-compose.yml up -d wtms
```

* 執行下列指令確定 selenium/standalone-chrome 和 flyhead/wtms images 正確下載 
```commandline
docker-compose images`
```


```shell
Container           Repository                   Tag                 Image Id            Size
rpa_chrome_1        selenium/standalone-chrome   latest              c59dc2754f9f        1.05GB
rpa_wtms_1          flyhead/wtms                 2021.0.1            2e089bfe0d47        127MB
```

* 執行下列指令確定 container 正確執行 

```shell
NAME                COMMAND                  SERVICE             STATUS              PORTS
rpa_chrome_1        "/opt/bin/entry_poin…"   chrome              running             0.0.0.0:4444->4444/tcp, :::4444->4444/tcp
rpa_wtms_1          "python /usr/local/s…"   wtms                running
```

 
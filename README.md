環境:
  python:3.12.4
必要包:
  paho-mqtt==2.1.0
  requests==2.32.3
  
利用docker運行它:
1. 進入mqtt-notifier資料夾，並開啟終端機

  #這個指令會根據 Dockerfile 建立一個名為 mqtt-notifier-app 的 Docker 映像。
2. 輸入: docker build -t mqtt-notifier-app .          

  #這個指令會在背景執行一個名為 mqtt-notifier-container 的容器，該容器使用剛才建立的 mqtt-notifier-app 鏡像。
3. 輸入: docker run -d --name mqtt-notifier-container mqtt-notifier-app  

  #查看應用程式的輸出日誌
4. 輸入: docker logs mqtt-notifier-container                             

import paho.mqtt.client as mqtt
import json
import requests
import smtplib
from email.mime.text import MIMEText
import time

# MQTT 消息處理
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("your/thingsboard/alert/topic")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload)
        device_name = payload.get("device")
        user_name = payload.get("userName")
        value = payload.get("value")
        line_tokens = payload.get("lineToken")#接收MQTT傳過來的接收者的LINE NOTIFY token
        user_mails = payload.get("userMail")#接收MQTT傳過來的接收者的gmail
        
        print(f"Received alert: Device={device_name}, User={user_name}, Value={value}")

        # 發送通知 line & mail
        
        # 確認 user_mails 是不是一個 list
        if isinstance(user_mails, list):
            # 如果是 list，每一個 mail 輪一遍傳送資料
            for user_mail in user_mails:
                send_email(f"Alert: {device_name}", f"Value: {value}", user_mail)
        else:
            # 如果不是 list，直接傳送資料
            send_email(f"Alert: {device_name}", f"Value: {value}", user_mails)
            
        # 確認 line_tokens 是不是一個 list
        if isinstance(line_tokens, list):
            # 如果是 list，每一個 line token 輪一遍傳送資料
            for line_token in line_tokens:
                send_line_notification(line_token, f"Alert from {device_name}: {value}")
        else:
            # 如果不是 list，直接傳送資料
            send_line_notification(line_tokens, f"Alert from {device_name}: {value}")

    except Exception as e:
        print(f"An error occurred while processing the message: {e}")

# 發送 LINE 通知
def send_line_notification(token, message):
    try:
        headers = {'Authorization': f'Bearer {token}'}
        data = {'message': message}
        response = requests.post('https://notify-api.line.me/api/notify', headers=headers, data=data)
        if response.status_code == 200:
            print("LINE notification sent successfully.")
        else:
            print(f"Failed to send LINE notification. Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to send LINE notification: {e}")

# 發送 Email 通知
def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    #輸入發送端的gmail帳號
    msg['From'] = 'gmail'
    msg['To'] = to_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            #以下兩處分別輸入發送端的gmail & google應用程式token
            server.login('gmail', 'google應用程式token')
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# 自動重啟邏輯
while True:
    try:
        # 初始化 MQTT 客戶端
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        #以下輸入你server的公網IP
        client.connect("輸入你的公網IP", 1883, 60)
        client.loop_forever()
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Restarting the client in 5 seconds...")
        time.sleep(5)

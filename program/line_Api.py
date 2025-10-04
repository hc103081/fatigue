from ngrok import ngrok_start
from line_bot import Line_bot
import threading


# 設定 LINE Api 的啟用狀態
state_open = False

# 向指定使用者 ID 發送訊息
user_id = 'U44a5e3e3cf9c8835a64bb1273b08f457'

def is_line_Api_open():
    """回傳 Line Api,Line bot 啟用狀態"""
    return state_open

def Start_line_Api():
    """啟動 ngrok 與 Flask"""
    global state_open
    state_open = True
    threading.Thread(target=Line_bot.app.run).start()
    threading.Thread(target=ngrok_start).start()

def input_line_message():
    while True:
        message = input("Enter message to send: ")
        print(Line_bot.sent_message(user_id, message))

if __name__ == "__main__":
    threading.Thread(target=Start_line_Api).start()
    threading.Thread(target=input_line_message).start()
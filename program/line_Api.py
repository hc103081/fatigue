from line_bot import Line_bot
import asyncio
import threading
from logs import Log

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

# 設定 LINE Api 的啟用狀態
state_open = False

# 向指定使用者 ID 發送訊息
user_id = 'U44a5e3e3cf9c8835a64bb1273b08f457'

# 設定 LINE Bot 的存取權杖與密鑰
access_token = 'ltwy2UPyvHTg7JAKyDWeRuQsF2wGkiGbe7zguLV9K6P5Gxbh8LyV8TgecpwefKmsVjDrv+pHqDIjzM2kuolIt2Co2xQ0PLnIPdw57yuKJ9+l2L7xhrnZAKKHyX+PVhlUcMtJ1zokKK8/HoJpbzvLsQdB04t89/1O/w1cDnyilFU='
secret = 'ccb3a53029a0ae2eda6fd90ed07e4fd0'

line_bot_api = LineBotApi(access_token)

# 控制發送訊息權限
status_can_sent_message = False

def is_line_Api_open():
    """回傳 Line Api,Line bot 啟用狀態"""
    return state_open

async def async_line_Api():
    """非同步函式，啟動 ngrok 與 Flask"""
    global state_open
    state_open = True
    line_bot_task = asyncio.to_thread(Line_bot.app.run)    
    try:
        await line_bot_task
    except Exception as e:
        Log.logger.warning(f"An error occurred: {e}")
    
# 傳送訊息給指定使用者
def sent_message(user_id, message):
    """
    Params:
        user_id: 要傳送訊息的使用者 ID
        message: 要傳送的訊息內容
    """
    if status_can_sent_message == False:
        Log.logger.info("控制權未開啟，無法傳送訊息!")
        return False
    
    line_bot_api.push_message(user_id, TextSendMessage(text=message))
    
def start_line_Api():
    """啟動 Line Api"""
    asyncio.run(async_line_Api())
    
def input_line_message():
    """
    測試用程式，等待使用者輸入訊息並發送至指定使用者
    """
    while True:
        message = input("Enter message to send: ")
        print(Line_bot.sent_message(user_id, message))


if __name__ == "__main__":
    t1 = threading.Thread(target=start_line_Api)
    t1.start()
    t1.join()

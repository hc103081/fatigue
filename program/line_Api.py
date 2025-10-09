from cv2 import line
from ngrok import ngrok_start
from line_bot import Line_bot
import asyncio
import threading

# 設定 LINE Api 的啟用狀態
state_open = False

# 向指定使用者 ID 發送訊息
user_id = 'U44a5e3e3cf9c8835a64bb1273b08f457'

def is_line_Api_open():
    """回傳 Line Api,Line bot 啟用狀態"""
    return state_open

async def async_line_Api():
    """非同步函式，啟動 ngrok 與 Flask"""
    global state_open
    state_open = True
    
    line_bot_task = asyncio.to_thread(Line_bot.app.run)
    ngrok_task = asyncio.to_thread(ngrok_start)
    
    try:
        await asyncio.gather(line_bot_task, ngrok_task)
    except Exception as e:
        print(f"An error occurred: {e}")
    
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

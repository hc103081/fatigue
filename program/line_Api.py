from dataclasses import dataclass
import time
from .logs import Log

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

class Line_Api:
    """
    自訂 Line Api 類別\n
    使用 open_sent_message 方法開啟傳送訊息功能\n
    透過 sent_message 方法傳送訊息
    """
    @dataclass
    class LineData:
        """
        整合 Line Bot 相關資料的類別
        """
        user_id: dict        # 要傳送訊息的使用者 ID
        access_token: str   # LINE Bot 的存取權杖
        secret: str          # LINE Bot 的密鑰
        state_open: bool = False    # 設定 LINE Api 的啟用狀態
        
        
    def __init__(self,user_id: dict = {},
                 access_token: str = '',
                 secret: str = '',
                 state_open: bool = False):
        self.data = self.LineData(
            user_id=user_id,
            access_token=access_token,
            secret=secret,
            state_open=state_open
        )
        self.line_bot_api = LineBotApi(self.data.access_token)
        self.status_can_sent_message = self.data.state_open  # 控制是否可以傳送訊息的狀態
        self.interval_sent_message = 10.0  # 預設傳送訊息間隔時間（秒）
        self.last_sent_time = 0.0  # 上次傳送訊息的時間戳
        self.messages = [] # 儲存訊息的列表

    def message(self, message: str):
        """
        新增訊息到列表中
        """
        self.messages.append(message)
        return self

    def sent(self, user_id) -> bool:
        """
        Params:
            user_id: 要傳送訊息的使用者 ID
        """
        if self.status_can_sent_message == False:
            Log.logger.debug("控制權未開啟，無法傳送訊息!")
            self.messages.clear() # 清空訊息列表
            return False
        
        # 檢查是否超過傳送訊息間隔時間
        current_time = time.time()
        if self.is_sent_cooldown():
            Log.logger.debug(f"未超過傳送訊息間隔時間 {self.interval_sent_message} 秒，等待中...")
            return False
        self.last_sent_time = current_time
        
        # 傳送訊息
        try:
            Log.logger.debug(f"傳送訊息至使用者 {user_id} : {self.messages}")
            self.line_bot_api.push_message(user_id, TextSendMessage(text='\n'.join(self.messages)))
            self.messages.clear() # 清空訊息列表
            return True
        except Exception as e:
            Log.logger.error(f"傳送訊息至使用者 {user_id} 時發生錯誤: {e}")
            return False
        
    def is_sent_cooldown(self) -> bool:
        """
        檢查是否處於傳送訊息冷卻時間內
        """
        current_time = time.time()
        return (current_time - self.last_sent_time) < self.interval_sent_message

    def open_sent_message(self):
        """
        開啟傳送訊息的功能
        """
        self.status_can_sent_message = True
        Log.logger.debug("已開啟傳送訊息功能")
        

if __name__ == "__main__":
    pass

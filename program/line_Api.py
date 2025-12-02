from dataclasses import dataclass
from flask import Flask
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
        state_open: bool    # 設定 LINE Api 的啟用狀態
        
        
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
        self.status_can_sent_message = False  # 控制是否可以傳送訊息的狀態

    def sent_message(self, user_id, message) -> bool:
        """
        Params:
            user_id: 要傳送訊息的使用者 ID
            message: 要傳送的訊息內容
        """
        if self.status_can_sent_message == False:
            Log.logger.info("控制權未開啟，無法傳送訊息!")
            print(message)
            return False
        
        try:
            Log.logger.info(f"傳送訊息至使用者 {user_id} : {message}")
            self.line_bot_api.push_message(user_id, TextSendMessage(text=message))
            return True
        except Exception as e:
            Log.logger.error(f"傳送訊息至使用者 {user_id} 時發生錯誤: {e}")
            return False
        
    def input_line_message(self):
        """
        測試用程式，等待使用者輸入訊息並發送至指定使用者
        """
        while True:
            message = input("Enter message to send: ")
            print(self.sent_message(self.data.user_id['Hong'], message))

    def open_sent_message(self):
        """
        開啟傳送訊息的功能
        """
        self.status_can_sent_message = True
        Log.logger.debug("已開啟傳送訊息功能")

if __name__ == "__main__":
    pass

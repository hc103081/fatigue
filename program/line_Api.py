from dataclasses import dataclass
from flask import Flask
from logs import Log

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

class Line_Api:
    """自訂 Line Api 類別"""
    @dataclass
    class LineData:
        """
        整合 Line Bot 相關資料的類別
        """
        user_id: dict        # 要傳送訊息的使用者 ID
        access_token: str   # LINE Bot 的存取權杖
        secret: str          # LINE Bot 的密鑰
        state_open: bool    # 設定 LINE Api 的啟用狀態
        status_can_sent_message: bool  # 控制是否可以傳送訊息的狀態
        
    def __init__(self):
        self.data = self.LineData(
            user_id={'Hong':'Uc588694833df79cafd6d19b3c2f505af',
                     'Kai': 'U44a5e3e3cf9c8835a64bb1273b08f457'
                     },
            access_token='ltwy2UPyvHTg7JAKyDWeRuQsF2wGkiGbe7zguLV9K6P5Gxbh8LyV8TgecpwefKmsVjDrv',
            secret='ccb3a53029a0ae2eda6fd90ed07e4fd0',
            state_open=False,
            status_can_sent_message=False
        )
        self.line_bot_api = LineBotApi(self.data.access_token)

    def get_data(self):
        return self.data

    def sent_message(self, user_id, message):
        """
        Params:
            user_id: 要傳送訊息的使用者 ID
            message: 要傳送的訊息內容
        """
        if self.data.status_can_sent_message == False:
            Log.logger.info("控制權未開啟，無法傳送訊息!")
            return False
        
        self.line_bot_api.push_message(user_id, TextSendMessage(text=message))
        
    def input_line_message(self):
        """
        測試用程式，等待使用者輸入訊息並發送至指定使用者
        """
        while True:
            message = input("Enter message to send: ")
            print(self.sent_message(self.data.user_id['Hong'], message))


if __name__ == "__main__":
    pass

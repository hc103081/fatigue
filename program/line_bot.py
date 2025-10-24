from flask import Flask, json, request
from .logs import Log
from .dataClass import ClassUnified

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

class Line_bot:
    """
    Line Bot 類別
    """
    def __init__(self, app: Flask, unified: ClassUnified):
        self.app = app
        self.line_data = unified.line_api.data
        self.app.add_url_rule("/", view_func=self.linebot, methods=['POST'])
        self.line_bot_api = LineBotApi(self.line_data.access_token)

    def linebot(self):
        body = request.get_data(as_text=True)                    # 取得收到的訊息內容
        try:
            json_data = json.loads(body)                         # json 格式化訊息內容

            # 確認 secret 是否正確
            handler = WebhookHandler(self.line_data.secret)
            # 加入回傳的 headers
            signature = request.headers['X-Line-Signature']
            handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
            # 取得回傳訊息的 Token
            tk = json_data['events'][0]['replyToken']
            # 取得 LINe 收到的訊息類型
            type = json_data['events'][0]['message']['type']
            if type == 'text':
                # 取得 LINE 收到的文字訊息
                msg = json_data['events'][0]['message']['text']
                Log.logger.debug(f'收到: {msg}')                                       # 印出內容
                reply = msg
            else:
                reply = '你傳的不是文字呦～'
            Log.logger.debug(f'reply: {reply}')
            self.line_bot_api.reply_message(tk, TextSendMessage(reply))  # 回傳訊息
        except Exception as e:
            # 如果發生錯誤，印出收到的內容
            Log.logger.warning(f"{body}+\n\n{e}")
        return 'OK'                                              # 驗證 Webhook 使用，不能省略

    def run(self):
        self.app.run()
        
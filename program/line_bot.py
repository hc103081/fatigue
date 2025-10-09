import re
from flask import Flask, json, request
from logs import Log


# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

# 設定 LINE Bot 的存取權杖與密鑰
access_token = 'ltwy2UPyvHTg7JAKyDWeRuQsF2wGkiGbe7zguLV9K6P5Gxbh8LyV8TgecpwefKmsVjDrv+pHqDIjzM2kuolIt2Co2xQ0PLnIPdw57yuKJ9+l2L7xhrnZAKKHyX+PVhlUcMtJ1zokKK8/HoJpbzvLsQdB04t89/1O/w1cDnyilFU='
secret = 'ccb3a53029a0ae2eda6fd90ed07e4fd0'

# 控制發送訊息權限
status_can_sent_message = False

line_bot_api = LineBotApi(access_token)

class Line_bot:
    """自訂 Line Bot 類別"""

    app = Flask(__name__)

    @app.route("/", methods=['POST'])
    def linebot():
        body = request.get_data(as_text=True)                    # 取得收到的訊息內容
        try:
            json_data = json.loads(body)                         # json 格式化訊息內容

            # 確認 secret 是否正確
            handler = WebhookHandler(secret)
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
            line_bot_api.reply_message(tk, TextSendMessage(reply))  # 回傳訊息
        except Exception as e:
            # 如果發生錯誤，印出收到的內容
            Log.logger.warning(f"{body}+\n\n{e}")
        return 'OK'                                              # 驗證 Webhook 使用，不能省略

    # 傳送訊息給指定使用者
    def sent_message(self,user_id, message):
        """
        Params:
            user_id: 要傳送訊息的使用者 ID
            message: 要傳送的訊息內容
        """
        if status_can_sent_message == False:
            Log.logger.info("控制權未開啟，無法傳送訊息!")
            return False
        
        line_bot_api.push_message(user_id, TextSendMessage(text=message))
        

    

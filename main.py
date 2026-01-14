from flask import Flask
import threading
import time
import json

# program class
from program import *
# 導入 dotenv 模組以載入環境變數
from dotenv import load_dotenv
load_dotenv() # 載入 .env 檔案中的環境變數

def main():
    app = Flask(__name__)
    GPIO.setmode(GPIO.BCM)

    init_components(app)
    
    try:
        thread_list: list[threading.Thread] = []
        
        # 啟動感測器更新執行緒
        update_sensor_thread = threading.Thread(target=update_sensor_data,
                                                args=(0.03,))
        thread_list.append(update_sensor_thread)
        
        # 啟動 Line Bot 執行緒 (已棄用)
        # line_bot_thread = threading.Thread(target=line_bot.run)
        # thread_list.append(line_bot_thread)
        
        # 啟動所有執行緒
        for thread in thread_list:
            thread.start()
        
        # 等待所有執行緒
        for thread in thread_list:
            thread.join()
        
    except Exception as e:
        Log.logger.warning(f"發生錯誤: {e}")

def init_components(app):
    """
    Params:
    初始化組件
        app (Flask): Flask 應用實例
    """
    global unified, mp3_player
    mp3_player = MP3Player()
    try:
        unified = ClassUnified()
        # 初始化攝像頭
        unified.camera = Camera(camera_index=0,
                        frame_width=640,
                        frame_height=480)
        
        # 初始化臉部分析器
        unified.fatigue = FaceAnalyzer(camera=unified.camera)
        
        # 初始化酒精感測器
        unified.alcohol = AlcoholSensor(use_mock=True,
                                limit=0.15)
        
        # 初始化 Line API
        unified.line_api = Line_Api(
                    {'Hong':'Uc588694833df79cafd6d19b3c2f505af',
                    'Kai': 'U44a5e3e3cf9c8835a64bb1273b08f457'
                    },
                    state_open=True,
                    )       
        
        # 初始化統一資料結構
        unified.data = DataUnified(
            alcohol=unified.alcohol.get_data(),
            fatigue=unified.fatigue.get_data(),
        )

        
    except Exception as e:
        Log.logger.warning(f"發生錯誤: {e}")
        raise e

def update_sensor_data(interval: float = 1.0):
    """
    更新感測器資料
    """
    def run_sensor():
        unified.alcohol.update()
    try:
        while True:
            sensor_thread = threading.Thread(target=run_sensor)
            fatigue_thread = threading.Thread(target=unified.fatigue.update)

            sensor_thread.start()
            fatigue_thread.start()

            sensor_thread.join()
            fatigue_thread.join()

            refresh_sensor_data()
            time.sleep(interval)
    except Exception as e:
        Log.logger.warning(f"發生錯誤: {e}")
        raise e

def refresh_sensor_data(alcohol_warning_interval: float = 60.0):
    """
    刷新感測器資料，並判斷是否需警示
    """
    unified.data = DataUnified(
        alcohol=unified.alcohol.get_data(),
        fatigue=unified.fatigue.get_data(),
    )
    print(f"Alcohol: {unified.data.alcohol.alcohol_value:.3f}, "
          f"Fatigue: {unified.data.fatigue.fatigue_score:.2f}",end="\r",flush=True)

    # 判斷是否在傳送訊息冷卻時間內
    if unified.line_api.is_sent_cooldown():
        return
    
    # 判斷酒精濃度是否超標
    if unified.data.alcohol.is_over_limit and time.time() - alcohol_warning_time_last > alcohol_warning_interval:
        alcohol_warning_time_last = time.time()
        # 播放酒精警示音效
        mp3_player.play("alcohol_warning", loops=0)
        # 發送 LINE 警示訊息
        unified.line_api.message(f"警告：酒精濃度超標，請勿駕駛！")

    # 判斷疲勞分數是否超過閾值
    if unified.data.fatigue.is_fatigued:
        # 播放疲勞警示音效
        mp3_player.play("fatigue_warning", loops=0)
        # 發送 LINE 警示訊息
        unified.line_api.message(f"警告：偵測到疲勞，請注意休息！")
    
    # 檢查是否有來自 GenAI 的深度分析回應
    genai_response = unified.fatigue.get_genai_response()
    if genai_response:
        try:
            # 解析專業報告 JSON
            report_data = json.loads(genai_response)
            
            # 填充 Flex Message 模板
            flex_template = {
              "type": "bubble",
              "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "📝 GenAI 疲勞回應分析",
                    "weight": "bold",
                    "size": "lg",
                    "align": "center"
                  }
                ]
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "📌 摘要",
                    "weight": "bold",
                    "size": "md"
                  },
                  {
                    "type": "text",
                    "text": report_data.get("summary", "無"),
                    "wrap": True,
                    "margin": "sm"
                  },
                  {
                    "type": "separator",
                    "margin": "md"
                  },
                  {
                    "type": "text",
                    "text": "🔎 分析",
                    "weight": "bold",
                    "size": "md",
                    "margin": "md"
                  },
                  {
                    "type": "text",
                    "text": report_data.get("analysis", "無"),
                    "wrap": True,
                    "margin": "sm"
                  },
                  {
                    "type": "separator",
                    "margin": "md"
                  },
                  {
                    "type": "text",
                    "text": "📊 結論",
                    "weight": "bold",
                    "size": "md",
                    "margin": "md"
                  },
                  {
                    "type": "text",
                    "wrap": True,
                    "margin": "sm",
                    "text": report_data.get("conclusion", "無")
                  },
                  {
                    "type": "separator",
                    "margin": "md"
                  },
                  {
                    "type": "text",
                    "text": "💡 建議",
                    "weight": "bold",
                    "size": "md",
                    "margin": "md"
                  },
                  {
                    "type": "text",
                    "text": report_data.get("suggestion", "無"),
                    "wrap": True,
                    "margin": "sm"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "style": "primary",
                    "color": "#4CAF50",
                    "action": {
                      "type": "uri",
                      "label": "查看完整分析",
                      "uri": "https://example.com/genai-fatigue-report"
                    }
                  }
                ]
              }
            }
            
            # 將 Flex Message 加入佇列
            unified.line_api.flex_message(flex_template)

        except (json.JSONDecodeError, KeyError) as e:
            # 如果 JSON 解析失敗或格式不符，退回發送純文字
            Log.logger.warning(f"解析 GenAI 回應失敗: {e}，將以純文字發送。")
            unified.line_api.message("AI 深度分析結果 (格式錯誤)：").message(genai_response)

    user_id = unified.line_api.data.user_id['Hong']
    # 一次性發送所有在佇列中的訊息 (文字 + Flex)
    if len(unified.line_api.messages) > 0:
        unified.line_api.sent(user_id)


if __name__ == "__main__":
    main()

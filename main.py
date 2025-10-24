from flask import Flask
import tkinter as tk
import threading
import time

# program class
from program import *

unified: ClassUnified = None

def main():
    app = Flask(__name__)
    GPIO.setmode(GPIO.BCM)

    init_components(app)
        
    try:
        thread_list: list[threading.Thread] = []
        
        # 啟動感測器更新執行緒
        update_sensor_thread = threading.Thread(target=update_sensor_data)
        thread_list.append(update_sensor_thread)
        
        # 啟動 Line Bot 執行緒
        line_bot_thread = threading.Thread(target=line_bot.run)
        thread_list.append(line_bot_thread)
        
        # 啟動 Web API 執行緒
        web_api_thread = threading.Thread(target=web_api.run)
        thread_list.append(web_api_thread)
        
        ngrok_thread = threading.Thread(target=ngrok.run)
        thread_list.append(ngrok_thread)
        
        # 啟動所有執行緒
        for thread in thread_list:
            thread.start()
        
        # 等待所有執行緒
        for thread in thread_list:
            thread.join()
        
    except Exception as e:
        Log.logger.warning(f"發生錯誤: {e}")

class Main:
    def get_sensor_data()->DataUnified:
        """
        取得感測器資料
        Returns:
            DataUnified: 包含感測器資料的 DataUnified 物件
        """
        global data
        return data

def init_components(app):
    """
    初始化組件
    Params:
        app (Flask): Flask 應用實例
    """
    global unified, line_bot, web_api, ui, ngrok
    use_mock = not check_hardware_connected()
    try:
        unified = ClassUnified(
            # 初始化臉部分析器
            fatigue = FaceAnalyzer(camera_index=0,
                                    threshold=0.3),
            
            # 初始化酒精感測器
            alcohol = AlcoholSensor(use_mock=use_mock,
                                    limit=0.15),
            
            # 初始化心率感測器
            heart = HeartRateSensor(use_mock=use_mock,
                                    threshold_low=60,
                                    threshold_high=100),
            
            # 初始化 Line API
            line_api = Line_Api(),
            
            data = None
        )
        
        
        unified.data = DataUnified(
            alcohol=unified.alcohol.get_data(),
            heart=unified.heart.get_data(),
            fatigue=unified.fatigue.get_data(),
        )
        
        # 初始化 ngrok
        ngrok = Ngrok()
        
        # 初始化 Line Bot
        line_bot = Line_bot(app,unified)
        
        # 初始化 Web API
        web_api = WebApi(app,unified)
        
        # 初始化 UI
        # root = tk.Tk()
        # ui = FatigueMonitorUI(root,unified)
        
    except Exception as e:
        Log.logger.warning(f"發生錯誤: {e}")
        raise e

def update_sensor_data():
    """
    更新感測器資料
    """
    def run_sensor():
        unified.alcohol.update()
        unified.heart.update()
    try:
        while True:
            sensor_thread = threading.Thread(target=run_sensor)
            fatigue_thread = threading.Thread(target=unified.fatigue.update)

            sensor_thread.start()
            fatigue_thread.start()

            sensor_thread.join()
            fatigue_thread.join()

            refresh_sensor_data()
            time.sleep(1)
    except Exception as e:
        Log.logger.warning(f"發生錯誤: {e}")
        raise e

def refresh_sensor_data():
    """
    刷新感測器資料
    """
    global data
    data = DataUnified(
        alcohol=unified.alcohol.get_data(),
        heart=unified.heart.get_data(),
        fatigue=unified.fatigue.get_data(),
    )
    
def check_hardware_connected():
    """
    檢查硬體是否連接
    Returns:
        True: 硬體已連接
        False: 硬體未連接
    """
    return False  # 預設為測試模式

if __name__ == "__main__":
    main()
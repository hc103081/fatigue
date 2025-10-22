import asyncio
from flask import Flask
import tkinter as tk
from alcohol import AlcoholSensor
from face_analyze import FaceAnalyzer
from gpio import GPIO
from heart import HeartRateSensor
import threading
import time
from web_Api import WebApi
from ngrok import ngrok_start
from dataClass import DataUnified
from line_Api import start_line_Api
from line_bot import Line_bot
from logs import Log
import multiprocessing
from ui import FatigueMonitorUI

_user_id = 'U44a5e3e3cf9c8835a64bb1273b08f457'

data = DataUnified()

def main():
    GPIO.setmode(GPIO.BCM)
    app = Flask(__name__)
    
    try:
        pass
    except Exception as e:
        Log.logger.warning(f"發生錯誤: {e}")


def get_sensor_data()->DataUnified:
    """
    取得感測器資料
    Returns:
        DataUnified: 包含感測器資料的 DataUnified 物件
    """
    global data
    return data

def check_hardware_connected():
    """
    檢查硬體是否連接
    Returns:
        True: 硬體已連接
        False: 硬體未連接
    """
    return False  # 預設為測試模式

def init_components(app):
    """
    初始化組件
    Params:
        app (Flask): Flask 應用實例
    """
    use_mock = not check_hardware_connected()
    try:
        global face_analyzer, alcohol_sensor,heart_sensor
        global line_bot, web_api, ui, root
        
        # 初始化臉部分析器
        face_analyzer = FaceAnalyzer(camera_index=0,
                                     threshold=0.3)
        
        # 初始化酒精感測器
        alcohol_sensor = AlcoholSensor(use_mock=use_mock,
                                       limit=0.15)
        
        # 初始化心率感測器
        heart_sensor = HeartRateSensor(use_mock=use_mock,
                                       threshold_low=60,
                                       threshold_high=100)
        
        # 初始化 Line Bot
        line_bot = Line_bot(app)
        
        # 初始化 Web API
        web_api = WebApi(app)
        
        # 初始化 UI
        root = tk.Tk()
        ui = FatigueMonitorUI(root)
        
    except Exception as e:
        Log.logger.warning(f"發生錯誤: {e}")
        raise e

async def async_monitor():
    """
    非同步監控任務
    持續監控感測器資料，並根據資料觸發相應的行動
    """
    try:
        while True:
            pass
    except KeyboardInterrupt:
        Log.logger.debug("監控任務停止")
        raise SystemExit
    except Exception as e:
        Log.logger.warning(f"發生錯誤: {e}")
        raise e

def update_sensor():
    """
    更新感測器資料
    """
    try:
        while True:
            alcohol_sensor.update()
            heart_sensor.update()
            face_analyzer.update()

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
        alcohol=alcohol_sensor.get_data(),
        heart=heart_sensor.get_data(),
        fatigue=face_analyzer.get_data()
    )

if __name__ == "__main__":
    main()
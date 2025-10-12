import asyncio
from alcohol import AlcoholSensor
from face_analyze import FaceAnalyzer
from gpio import GPIO
from heart import HeartRateSensor
from face_analyze import FaceAnalyzer
import threading
import time
from line_Api import start_line_Api
from line_bot import Line_bot
from logs import Log
import multiprocessing

# Line用戶端user_id
_user_id = 'U44a5e3e3cf9c8835a64bb1273b08f457'  

# 設定定時任務開始時間
start_time = 8

# 設定定時任務結束時間
end_time = 20

def main():
    global line_bot
    # 設置GPIO模式
    GPIO.setmode(GPIO.BCM)
    
    # 啟用Line_bot
    line_bot = Line_bot()
    
    # 主程式循環
    try:
        with Monitor() as monitor:
            # 啟動定時任務
            schedule_thread = threading.Thread(target=set_scheduled, 
                            args=(_user_id,)
                            )
            
            # 啟動駕駛狀態監控
            monitor_thread = threading.Thread(target=monitor.start,
                            args=(_user_id,)
                            )
            
            # 啟動Line API
            line_api_thread = threading.Thread(target=start_line_Api,
                            args=()
                            )
            
            # 啟動並等待
            schedule_thread.start()
            monitor_thread.start()
            line_api_thread.start()
            
            schedule_thread.join()
            monitor_thread.join()
            line_api_thread.join()

    except Exception as e:
        Log.logger.warning(f"發生錯誤: {e}")

class Monitor():
    """
    監控類別，用於監控感測器數據並發送警告消息。
    """
    def __init__(self):
        """
        初始化套件
        """
        self.cd = 0.0  # 冷卻時間
        self.cd_time_max = 1.0  # 冷卻時間最大值
        self.last_trigger_time = None   # 上次觸發時間

        # 檢查是否連接硬體
        use_mock = not self.check_hardware_connected()
        try:
            # 初始化感測器
            self.face_analyzer = FaceAnalyzer()
            self.alcohol_sensor = AlcoholSensor(1, use_mock=use_mock)
            self.heart_sensor = HeartRateSensor(use_mock=use_mock)
            
        except Exception as e:
            Log.logger.warning(f"發生錯誤: {e}")
            raise e
    

    # 監控感測器數據並發送警告消息
    def start(self,user_id):
        """
        啟用感測器與監控
        """
        asyncio.run(self.async_monitor(user_id))

    async def async_monitor(self,user_id):
        try:
            while True:
                loop = asyncio.get_event_loop()
                
                # 刷新所有數據
                alcohol_update = asyncio.to_thread(self.alcohol_sensor.update)
                heart_update = asyncio.to_thread(self.heart_sensor.update)
                face_analyzer_update = loop.run_in_executor(None, self.face_analyzer.update)
                
                # 等待所有感測器數據
                alcohol_ok = await alcohol_update
                heart_ok = await heart_update
                face_ok = await face_analyzer_update
        
                # 讀取感測器數據
                alcohol_task = asyncio.to_thread(self.alcohol_sensor.get_alcohol)
                heart_task = asyncio.to_thread(self.heart_sensor.get_average)
                face_analyzer_task = asyncio.to_thread(self.face_analyzer.get_fatigue_score) if face_ok else None
                
                # 判斷是否超過限制
                self.review(user_id)
                
                # 等待n秒後再次監控
                await asyncio.sleep(0.1)
                
        except KeyboardInterrupt:
            Log.logger.debug("監控任務停止")
            raise SystemExit
        except Exception as e:
            Log.logger.warning(f"發生錯誤: {e}")
            raise e

    def review(self,user_id):
        """
        審核感測器數據，判斷是否超過限制並發送警告消息
        """
        # 判斷是否再在冷卻
        if self.is_in_cd():
            return 
        else:
            self.last_trigger_time = time.time()
        
        # 如果酒精濃度超過限制，發送警告消息
        if self.alcohol_sensor.is_over_limit():
            line_bot.sent_message(user_id, "警告: 酒精濃度過高，請勿駕駛！")
            Log.logger.info("警告: 酒精濃度過高，請勿駕駛！")
            
        # 如果心率異常，發送警告消息
        if self.heart_sensor.is_normal():
            line_bot.sent_message(user_id, "警告: 心率異常，請注意休息！")
            Log.logger.info("警告: 心率異常，請注意休息！")
        
        # 判斷人臉偵測到疲勞
        if self.face_analyzer.is_fatigued():
            line_bot.sent_message(user_id, "警告: 人臉偵測到疲勞，請注意休息！")
            Log.logger.info("警告: 人臉偵測到疲勞，請注意休息！")
    
    def is_in_cd(self):
        """
        判斷是否在冷卻時間內
        Returns:
            True: 冷卻中
            False: 不在冷卻時間內
        """
        now = time.time()
    
        # 判斷是否在冷卻時間內
        if self.last_trigger_time is None:
            return False  
        
        return (now - self.last_trigger_time) < self.cd_time_max  # 冷卻中
    
    def check_hardware_connected(self):
        """
        檢查硬體是否連接
        Returns:
            True: 硬體已連接
            False: 硬體未連接
        """
        # 這裡可以根據實際硬體檢查方式實作
        # 例如嘗試讀取硬體，失敗則回傳 False
        return False  # 預設為測試模式
            
    # 獲取當前狀態消息
    def get_status_msg(self):
        """
        獲取當前狀態消息
        Returns:
            str: 包含疲勞、心率、酒精濃度的狀態消息
        """
        # 生成感測
        heart_rate = self.heart_sensor.get_latest()
        alcohol_level = self.alcohol_sensor.get_alcohol()

        # 狀態判斷
        status_msg = f"疲倦:, 心率:{heart_rate}, 酒精:{alcohol_level}"
        return status_msg
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.face_analyzer.__exit__(exc_type, exc_val, exc_tb)
        self.alcohol_sensor.__exit__(exc_type, exc_val, exc_tb)
        self.heart_sensor.__exit__(exc_type, exc_val, exc_tb)
        pass
        

    

# 設置定時任務
def set_scheduled(user_id):
    # schedule.every(1).minutes.do(send_message,user_id=user_id)
    while True:
        # 取得當地時間
        time_now = time.localtime().tm_hour

        time.sleep(1000)

# 向Line用戶端發送消息
def send_message(user_id):
    line_bot.sent_message(user_id, Monitor.get_status_msg())


if __name__ == "__main__":
    main()


    def check_hardware_connected(self):
        # 這裡可以根據實際硬體檢查方式實作
        return False  # 預設為測試模式
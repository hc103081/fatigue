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
    def __init__(self):
        """
        初始化套件
        """
        # 判斷冷卻時間
        self.cd = 0.0
        
        # 冷卻時間上限
        self.cd_time_max = 1.0
        
        # 上次觸發時間
        self.last_trigger_time = None
        
        try:
            # 啟動人臉分析器
            self.face_analyzer = FaceAnalyzer()
            
            # 啟動酒精感測器
            self.alcohol_sensor = AlcoholSensor(1)
            
            # 啟動心率感測器
            self.heart_sensor = HeartRateSensor()
            
        
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
        """
        監控感測器數據並發送警告消息
        """
        try:
            while True:
                loop = asyncio.get_event_loop()
                
                # 刷新所有數據
                alcohol_update = asyncio.to_thread(self.alcohol_sensor.update)
                heart_update = asyncio.to_thread(self.heart_sensor.update)
                face_analyzer_update = loop.run_in_executor(None, self.face_analyzer.update)
                
                # 等待所有感測器數據
                # await asyncio.gather(alcohol_update, heart_update, face_analyzer_update)
                
                # 讀取感測器數據
                alcohol_task = asyncio.to_thread(self.alcohol_sensor.get_alcohol)
                heart_task = asyncio.to_thread(self.heart_sensor.get_average)
                face_analyzer_task = asyncio.to_thread(self.face_analyzer.get_fatigue_score)
                
                # 等待所有感測器數據讀取完成
                # data = await asyncio.gather(alcohol_task, heart_task, face_analyzer_task)
                
                # 判斷是否超過限制
                self.review(user_id)
                
                # 等待n秒後再次監控
                # await asyncio.sleep(0.1)
                
        except KeyboardInterrupt:
            Log.logger.debug("監控任務停止")
            raise SystemExit
        except Exception as e:
            Log.logger.warning(f"發生錯誤: {e}")
            raise e

    def review(self,user_id):
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
        now = time.time()
    
        # 判斷是否在冷卻時間內
        if self.last_trigger_time is None:
            return False  
        
        return (now - self.last_trigger_time) < self.cd_time_max  # 冷卻中
            
    # 獲取當前狀態消息
    def get_status_msg(self):

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

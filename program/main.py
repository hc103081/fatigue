from alcohol import AlcoholSensor
from camera import Camera
from face_analyze import FaceAnalyzer
from gpio import GPIO
from heart import HeartRateSensor
from face_analyze import FaceAnalyzer
import threading
import time
from line_bot import Line_bot
import schedule

# Line用戶端user_id
_user_id = 'U44a5e3e3cf9c8835a64bb1273b08f457'  

# 設定定時任務開始時間
start_time = 8

# 設定定時任務結束時間
end_time = 20

def main():

    # 設置GPIO模式
    GPIO.setmode(GPIO.BCM)
    
    # 初始化攝像頭、感測器、GPIO
    global camera
    camera = Camera(0)
    global heart_sensor
    heart_sensor = HeartRateSensor()
    global alcohol_sensor
    alcohol_sensor = AlcoholSensor(0)
    global face_analyzer
    face_analyzer = FaceAnalyzer()
    
    # 初始化Line_bot
    global line_bot
    line_bot = Line_bot()

    # 主程式循環
    try:
        # 啟動定時任務
        threading.Thread(target=set_scheduled, 
                        args=(_user_id,)
                        ).start()
        
        # 啟動駕駛狀態監控
        threading.Thread(target=monitor,
                        args=(_user_id,)
                        ).start()
        
    except KeyboardInterrupt:
        print("程式終止")
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        camera.close()
        GPIO.cleanup()
        

# 監控感測器數據並發送警告消息
def monitor(user_id):
    while True:
        # 如果酒精濃度超過限制，發送警告消息
        if alcohol_sensor.is_over_limit():
            line_bot.sent_message(user_id, "警告: 酒精濃度過高，請勿駕駛！")
            time.sleep(10000)
        # 如果心率異常，發送警告消息
        if heart_sensor.is_normal():
            line_bot.sent_message(user_id, "警告: 心率異常，請注意休息！")
            time.sleep(10000)
        # 判斷人臉偵測到疲勞
        if face_analyzer.get_fatigue(camera.get_frame()) > 0.8:
            line_bot.sent_message(user_id, "警告: 人臉偵測到疲勞，請注意休息！")
            time.sleep(10000)
        time.sleep(1000)

# 獲取當前狀態消息
def get_status_msg():
    # 讀取影像
    frame = camera.get_frame()
    if frame is None:
        print("無法讀取影像")
        return None

    # 脸部特徵分析
    face_analyzer = FaceAnalyzer()

    # 生成感測
    heart_rate = heart_sensor.get_latest()
    alcohol_level = alcohol_sensor.get_alcohol()

    # 狀態判斷
    status_msg = f"疲倦:, 心率:{heart_rate}, 酒精:{alcohol_level}"
    return status_msg

# 設置定時任務
def set_scheduled(user_id):
    schedule.every(1).hours.do(send_message,user_id=user_id)
    while True:
        # 取得當地時間
        time_now = time.localtime().tm_hour
        
        # 判斷是否在設定的時間範圍內
        if start_time <= time_now < end_time:
            schedule.run_pending()
        
        time.sleep(1000)

# 向Line用戶端發送消息
def send_message(user_id):
    line_bot.sent_message(user_id, get_status_msg())

if __name__ == "__main__":
    main()

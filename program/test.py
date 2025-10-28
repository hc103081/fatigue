from logs import Log


# Line測試
def line_test():
    from line_bot import Line_bot

    line_bot = Line_bot()
    id = ['Uc588694833df79cafd6d19b3c2f505af',
          'U44a5e3e3cf9c8835a64bb1273b08f457']
    
    for i in range(1):
        line_bot.sent_message(id[0],'gay')
        
# gpio測試
def gpio_test():
    try:
        import RPi.GPIO as GPIO     # type: ignore
    except ImportError:
        from gpio import GPIO as GPIO
    pin = 26
    
    print("start")
    try:
        state = '0'
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)  # 設定 GPIO 為輸出模式 控制攝像頭開關
        while True:
            state = input("Enter state:")
            if(state == '1'):
                GPIO.output(pin, GPIO.HIGH)      # 預設攝像頭為開啟狀態
                print(GPIO.input(26))
                
            elif(state == '0'):
                GPIO.output(pin, GPIO.LOW)      # 預設攝像頭為開啟狀態
            else:
                break
            print(GPIO.input(26))
            
    except AttributeError:
        raise RuntimeError("無法")
    finally:
        GPIO.output(pin, GPIO.LOW)   # 關閉攝像頭
        GPIO.cleanup()               # 清理 GPIO 狀態
    print("end")
    
# 相機測試
def camera_test():
    from face_analyze import FaceAnalyzer
    from camera import Camera
    import cv2
    
    with FaceAnalyzer() as face_analyzer:
        while True: 

            # 从摄像头读取一帧
            frame = face_analyzer.get_frame()
            
            # 显示帧
            cv2.imshow('USB Camera', frame)
            # 按下 'q' 键退出循环
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
def camera_test2():
    import cv2
    import os
    # os.environ["QT_QPA_PLATFORM"] = "xcb"

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
 
    while True:
        ret, frame = cap.read()
        if not ret:
            print("have no camera")
            break
        cv2.imshow("USB Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def face_analyze_test3():
    from face_analyze import FaceAnalyzer
    import cv2
    
    with FaceAnalyzer() as face_analyzer:
        while True:
            face_analyzer.update()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
def face_analyze_test2():
    from face_analyze import FaceAnalyzer
    import cv2
    import numpy as np

    with FaceAnalyzer() as face_analyzer:
        while True:
            frame = face_analyzer.get_frame()
            if frame is None:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            equa = cv2.equalizeHist(gray)

            # 強制轉型與驗證
            if not isinstance(equa, np.ndarray):
                raise TypeError("equa 不是 numpy 陣列")
            if equa.dtype != np.uint8:
                equa = equa.astype(np.uint8)
            if len(equa.shape) != 2:
                raise ValueError("equa 必須是灰階圖像 (H, W)")

            faces = face_analyzer.detector(equa, 0)

            # landmark 預測
            for i, face in enumerate(faces):
                shape = face_analyzer.predictor(gray)
                print(f"人臉 {i+1} 的關鍵點座標：")
                for idx in range(68):
                    x = shape.part(idx).x
                    y = shape.part(idx).y
                    print(f"  Point {idx}: ({x}, {y})")

            cv2.imshow("Fatigue Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
def face_analyze_test():
    from face_analyze import FaceAnalyzer
    import cv2
    
    with FaceAnalyzer() as face_analyzer:
        while True:
            # 取得畫面並進行處理
            frame = face_analyzer.get_frame()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            equa = cv2.equalizeHist(gray)
            
            # 偵測人臉
            faces = face_analyzer.detector(equa)
            
            for face in faces:
                # 偵測特徵點
                shape = face_analyzer.predictor(equa, face)
                score = face_analyzer.get_fatigue_score()
                fatigue = face_analyzer.is_fatigued(score)
                
                # 畫左眼 (特徵點 36–41)
                for i in range(36, 42):
                    x, y = shape.part(i).x, shape.part(i).y
                    cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

                # 畫右眼 (特徵點 42–47)
                for i in range(42, 48):
                    x, y = shape.part(i).x, shape.part(i).y
                    cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

                # 畫嘴巴 (特徵點 48–67)
                for i in range(48, 68):
                    x, y = shape.part(i).x, shape.part(i).y
                    cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

                # 顯示結果W
                text = f"Fatigue Score: {score:.2f} | Fatigued: {fatigue}"
                cv2.putText(frame, text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255) if fatigue else (0, 255, 0), 2)
                
                
            cv2.imshow("Fatigue Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
def flask_test():
    from web_Api import WebApi
    import threading
    from ngrok import ngrok_start
    from line_bot import Line_bot

    with WebApi() as web_thread:
        app_thread = threading.Thread(target=web_thread.app.run)
        app_thread.start()
        
        line_thread = threading.Thread(target=Line_bot.app.run)
        line_thread.start()
        
def alcohol_test():
    from gpiozero import MCP3008
    import time

    # MCP3008 的 CH0 通道
    sensor = MCP3008(channel=0)
    
    while True:
        value = sensor.value  # 取得 0~1 之間的類比值
        print(f"MQ3感測器數值: {value:.3f}")
        time.sleep(1)

def mq3_test():
    import spidev
    import time

    spi = spidev.SpiDev()
    spi.open(0, 0)

    def read_channel(channel):
        adc = spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def convert_volts(data, places):
        volts = (data * 3.3) / 1023
        return round(volts, places)

    while True:
        value = read_channel(0)
        voltage = convert_volts(value, 2)
        print(f"MQ3 Value: {value}, Voltage: {voltage}V")
        time.sleep(1)

        
if __name__ == "__main__":
    # line_test()
    # face_analyze_test2()
    # face_analyze_test()
    # flask_test()
    # alcohol_test()
    mq3_test()
    pass
    


# 设置判断参数
# 初始化计数器
# 遍历每一帧
# 检测人脸
# 遍历每一个检测到的人脸
# 获取坐标
# 分别计算ear值
# 算一个平均的
# 绘制眼睛区域
# 检查是否满足阈值
# 显示

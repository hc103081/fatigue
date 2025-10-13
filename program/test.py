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
            cv2.imshow('摄像头画面', frame)
            # 按下 'q' 键退出循环
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
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
    
    with FaceAnalyzer() as face_analyzer:
        while True:
            frame = face_analyzer.get_frame()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            equa = cv2.equalizeHist(gray)
            faces = face_analyzer.detector(equa,0)
            
            # 取出所有偵測的結果
            for i, d in enumerate(faces):
                x1 = d.left()
                y1 = d.top()
                x2 = d.right()
                y2 = d.bottom()

                # 以方框標示偵測的人臉
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4, cv2.LINE_AA)
                    
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
                face_analyzer.set_landmarks_points(shape)
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
                

if __name__ == "__main__":
    # line_test()
    camera_test()
    # face_analyze_test()
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

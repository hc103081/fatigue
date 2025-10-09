
def line_test():
    from line_bot import Line_bot

    line_bot = Line_bot()
    id = 'U44a5e3e3cf9c8835a64bb1273b08f457'
    for i in range(5):
        line_bot.sent_message(id,'gay')
        
# 測試程式
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
    
def camera_test():
    from camera import Camera
    import cv2
    
    camera = Camera()
    while True:
        # 从摄像头读取一帧
        frame = camera.get_frame()
        
        # 显示帧
        cv2.imshow('摄像头画面', frame)
        # 按下 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # 释放摄像头并关闭所有窗口
    cv2.destroyAllWindows()
<<<<<<< HEAD

=======
    


def camera_test_asnyc():
    pass
>>>>>>> main
    

def test_asnyc():
    pass




if __name__ == "__main__":
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

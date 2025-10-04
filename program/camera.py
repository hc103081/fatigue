import cv2
from gpio import GPIO

class Camera:
    """攝像頭模組"""

    def __init__(self,pin, camera_index=0):
        """ 
        初始化攝像頭 
        Params:
            pin: 控制攝像頭開關的 GPIO 腳位
            camera_index: 攝像頭索引 預設為 0      
        """
        self.camera_index = camera_index
        self.pin = pin
        try:
            GPIO.setup(self.pin, GPIO.OUT)  # 設定 GPIO 為輸出模式 控制攝像頭開關
            GPIO.output(self.pin, GPIO.HIGH)      # 預設攝像頭為開啟狀態
            self.cap = cv2.VideoCapture(camera_index)  # 初始化攝像頭
            
        except AttributeError:
            raise RuntimeError("無法初始化攝像頭，請檢查攝像頭是否連接正確")
        finally:
            self.cap.release()                # 釋放之前的攝像頭資源
            GPIO.output(self.pin, GPIO.LOW)   # 關閉攝像頭
            GPIO.cleanup()                    # 清理 GPIO 狀態
        
    # 讀取一幀影像
    def get_frame(self):
        """ 
        讀取並回傳一幀影像\n
        如果讀取失敗 回傳 None
        """
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    # 關閉攝像頭
    def close(self):
        """ 關閉攝像頭 """
        GPIO.output(self.pin, GPIO.LOW)    # 關閉攝像頭

        
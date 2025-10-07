import cv2

class Camera:
    """攝像頭模組"""

    def __init__(self, camera_index=0):
        """ 
        初始化攝像頭 
        Params:
            camera_index: 攝像頭索引 預設為 0      
        """
        self.camera_index = camera_index
        try:
            self.cap = cv2.VideoCapture(camera_index)  # 初始化攝像頭
            
        except AttributeError:
            raise RuntimeError("無法初始化攝像頭，請檢查攝像頭是否連接正確")
        
        
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
        
        
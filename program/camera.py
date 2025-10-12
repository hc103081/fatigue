import time
import cv2
from logs import Log

class Camera:
    """攝像頭模組"""

    def __init__(self, camera_index=0):
        """ 
        初始化攝像頭 
        Params:
            camera_index: 攝像頭索引 預設為 0      
        """
        self.camera_index = camera_index
        self.last_log_time = 0  # 新增：記錄上一次 log 的時間
        
        # 記錄日志的時間間隔，單位：秒
        self.log_interval = 10  

        try:
            self.cap = cv2.VideoCapture(camera_index)  # 初始化攝像頭
            
        except cv2.error:
            raise Exception("無法初始化攝像頭")
        
        
     # 讀取一幀影像
    def get_frame(self):
        """ 
        讀取並回傳一幀影像\n
        如果讀取失敗 回傳 None
        """
        ret, frame = self.cap.read()
        if not ret:
            now = time.time()
            # 只在超過 log_interval 秒才記錄
            if now - self.last_log_time > self.log_interval:
                Log.logger.warning("未取得影像 frame，跳過分析")
                self.last_log_time = now
            return None
        return frame
    
    # 關閉攝像頭
    def close(self):
        """ 關閉攝像頭 """
        if self.cap.isOpened():
            self.cap.release()
            cv2.destroyAllWindows()
    
    def __enter__(self):
        """ 支持 with 語句 """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """ 退出 with 語句時自動關閉攝像頭 """
        self.close()
        if exc_type is not None:
            Log.logger.warning(exc_type, exc_val, exc_tb)
            return False  # 攔截例外並回傳 False
        Log.logger.debug("camera closed")
        return True  # 正常結束 with 語句
    
        
        
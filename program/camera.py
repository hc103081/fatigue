from dataclasses import dataclass
import time
import cv2
from .logs import Log
import os

class Camera:
    """攝像頭模組"""    
    @dataclass
    class CameraData():
        """
        攝像頭數據
        """
        frame: any
        is_camera_open: bool

    def __init__(self, camera_index=0,frame_width=640,frame_height=480):
        """ 
        初始化攝像頭 
        Params:
            camera_index: 攝像頭索引 預設為 0      
        """
        self.data = self.CameraData(
            frame=None,
            is_camera_open=False
        )
        os.environ["QT_QPA_PLATFORM"] = "xcb"
        self.camera_index = camera_index
        self.camera_last_log_time = 0      # 新增：記錄上一次 log 的時間
        self.camera_log_interval = 10      # 記錄日志的時間間隔，單位：秒

        try:
            self.cap = cv2.VideoCapture(camera_index)  # 初始化攝像頭
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
            
            
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
            # 只在超過 camera_log_interval 秒才記錄
            if now - self.camera_last_log_time > self.camera_log_interval:
                Log.logger.warning("未取得影像 frame，跳過分析")
                self.camera_last_log_time = now
            return None
        return frame
    
    def set_frame_size(self,frame_width,frame_height):
        """
        設定攝像頭影像尺寸
        Params:
            frame_width: 影像寬度
            frame_height: 影像高度
        """
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    
    def run(self):
        """ 持續讀取影像並更新 data.frame """
        while self.data.is_camera_open:
            frame = self.get_frame()
            if frame is not None:
                self.data.frame = frame
    
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
            Log.logger.warning(f'{exc_type}, {exc_val}, {exc_tb}')
            return False  # 攔截例外並回傳 False
        Log.logger.debug("camera closed")
        return True  # 正常結束 with 語句
    
        
        
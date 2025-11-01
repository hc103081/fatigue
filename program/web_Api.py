import base64
from dataclasses import asdict
import cv2
import requests
import time
from .logs import Log
from .dataClass import DataUnified, ClassUnified

class WebApi():
    """Web API 服務"""
    def __init__(self,unified:ClassUnified):
        self.unified = unified
        
    def send_dataClass(self, interval=1):
        """
        定時上傳 dataclass 統一資料至 Render API
        interval: 上傳間隔秒數
        """
        while True:
            data = self.get_dataClass_dict()
            try:
                requests.post('https://fatigue-m68t.onrender.com/upload_dataClass', json=data)
            except Exception as e:
                Log.logger.warning(f"send_dataClass failed: {e}")
            time.sleep(interval)

    def send_image(self, interval=1):
        """
        定時上傳壓縮影像至 Render API
        interval: 上傳間隔秒數
        """
        while True:
            if not self.unified.camera.data.is_camera_open:
                continue

            frame = self.unified.camera.get_frame()

            if frame is None:
                Log.logger.warning("get frame failed")
                continue

            # 壓縮尺寸
            frame = cv2.resize(frame, (320, 240))
            # JPEG 壓縮品質 60
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            try:
                requests.post('https://fatigue-m68t.onrender.com/upload_image', json={'image_base64': img_base64})
            except Exception as e:
                Log.logger.warning(f"send_image failed: {e}")
            time.sleep(interval)  # 可自訂推送速率

    def get_dataClass_dict(self):
        """
        取得統一資料，並移除不可序列化欄位
        """
        dict_data = asdict(self.unified.data)
        # 移除 fatigue/camera 內的 frame 欄位（如有）
        if "fatigue" in dict_data and "frame" in dict_data["fatigue"]:
            dict_data["fatigue"]["frame"] = None
        if "camera" in dict_data and "frame" in dict_data["camera"]:
            dict_data["camera"]["frame"] = None
        return dict_data

    
            
    def run(self, interval_data=1, interval_image=1):
        """
        啟動 Web API 伺服器
        """
        import threading
        
        
        send_image_thread = threading.Thread(target=self.send_image, args=(interval_image,), daemon=True)
        send_dataClass_thread = threading.Thread(target=self.send_dataClass, args=(interval_data,), daemon=True)
        
        threads = [send_image_thread, send_dataClass_thread]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
            

        
if __name__ == "__main__":
    pass
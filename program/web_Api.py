import socketio
import time
import base64
import cv2
from dataclasses import asdict
from .logs import Log
from .dataClass import DataUnified, ClassUnified

class WebApi():
    """Web API 服務（WebSocket 客戶端）"""
    def __init__(self, unified: ClassUnified, 
                 server_url='https://fatigue-m68t.onrender.com'):
        self.unified = unified
        self.server_url = server_url
        self.sio = socketio.Client()
        self.connected = False

        @self.sio.event
        def connect():
            print("SocketIO connected!")
            self.connected = True

        @self.sio.event
        def disconnect():
            print("SocketIO disconnected!")
            self.connected = False

    def send_dataClass(self, interval=1):
        """
        定時推送 dataclass 統一資料至 Render WebSocket
        interval: 推送間隔秒數
        """
        while True:
            data = self.get_dataClass_dict()
            if self.connected:
                try:
                    self.sio.emit('dataClass_update',
                                  {"success": True, "data": data},
                                  broadcast=True)

                except Exception as e:
                    Log.logger.warning(f"send_dataClass failed: {e}")
            else:
                Log.logger.warning("SocketIO 尚未連線，無法推送 dataClass")
            time.sleep(interval)

    def send_image(self, interval=1):
        """
        定時推送壓縮影像至 Render WebSocket
        interval: 推送間隔秒數
        """
        while True:
            if not self.unified.camera.data.is_camera_open:
                time.sleep(interval)
                continue

            frame = self.unified.camera.get_frame()
            if frame is None:
                Log.logger.warning("get frame failed")
                time.sleep(interval)
                continue

            # 壓縮尺寸
            frame = cv2.resize(frame, (320, 240))
            # JPEG 壓縮品質 60
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            if self.connected:
                try:
                    self.sio.emit('upload_image', {"image": img_base64})
                except Exception as e:
                    Log.logger.warning(f"send_image failed: {e}")
            else:
                Log.logger.warning("SocketIO 尚未連線，無法推送 image")
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
        啟動 Web API 服務（資料與影像推送執行緒）
        """
        import threading

        # 持續嘗試連線直到成功
        while not self.connected:
            try:
                self.sio.connect(self.server_url)
                if self.connected:
                    Log.logger.info(f"WebSocket 連線成功: {self.server_url}")
            except Exception as e:
                Log.logger.warning(f"WebSocket 連線失敗: {e}")
            if not self.connected:
                time.sleep(5)

        send_image_thread = threading.Thread(target=self.send_image, args=(interval_image,), daemon=True)
        send_dataClass_thread = threading.Thread(target=self.send_dataClass, args=(interval_data,), daemon=True)
        threads = [send_image_thread, send_dataClass_thread]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    pass
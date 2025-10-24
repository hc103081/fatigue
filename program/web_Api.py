from dataclasses import asdict
import cv2
from flask import Flask, Response, jsonify
from .logs import Log
from .dataClass import DataUnified, ClassUnified
import threading

class WebApi():
    """Web API 服務"""
    def __init__(self, app: Flask,unified:ClassUnified):
        super().__init__()
        self.app = app
        self.unified = unified
        self.app.add_url_rule('/get_dataClass',
                              view_func=self.get_dataClass,
                              methods=['GET'])
        self.app.add_url_rule('/video_feed',
                              view_func=self.video_feed,
                              methods=['GET'])

    def get_dataClass(self):
        # 這裡取得感測資料
        data = self.unified.data
        return jsonify(asdict(data))
    
    def video_feed(self):
        return Response(self.get_frame_encoded(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def get_frame_encoded(self):
        while True:
            frame = self.unified.fatigue.get_frame()
            if frame is None:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    def run(self):
        """
        啟動 Web API 伺服器
        """
        self.app.run()
    
if __name__ == "__main__":
    pass
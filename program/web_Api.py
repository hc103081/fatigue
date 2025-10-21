from dataclasses import asdict
import cv2
from flask import Flask, Response, jsonify
from logs import Log
from dataClass import SensorData
from ngrok import ngrok_start
import threading
from camera import Camera

class WebApi():
    """Web API 服務"""
    def __init__(self, app: Flask):
        super().__init__()
        self.camera = Camera()
        self.app = app
        self.app.add_url_rule('/get_dataClass',
                              view_func=self.get_dataClass,
                              methods=['GET'])
        self.app.add_url_rule('/video_feed',
                              view_func=self.video_feed,
                              methods=['GET'])

    def get_dataClass(self):
        # 這裡取得感測資料
        data = SensorData(
            alcohol_level=0.05,
            is_alcohol=True,
            heart_rate=85,
            is_heart_rate_normal=True,
            fatigue_score=0.3,
            is_fatigued=False,
            camera_ok=True
        )
        return jsonify(asdict(data))
    
    def video_feed(self):
        return Response(self.get_frame_encoded(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def get_frame_encoded(self):
        while True:
            frame = self.camera.get_frame()
            if frame is None:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    def __enter__(self):
        return super().__enter__()
    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
    
if __name__ == "__main__":
    app = Flask(__name__)
    with WebApi(app) as web_thread:
        app_thread = threading.Thread(target=web_thread.app.run)
        app_thread.start()
    
        ngrok_thread = threading.Thread(target=ngrok_start)
        ngrok_thread.start()
from dataclasses import asdict
import cv2
from flask import Flask, Response, jsonify
from logs import Log
from dataClass import SensorData
from ngrok import ngrok_start
import threading

app = Flask(__name__)

@app.route('/get_dataClass', methods=['GET', 'POST'])
def get_dataClass():
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

def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed', methods=['GET'])
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app_thread = threading.Thread(target=app.run)
    app_thread.start()
    
    ngrok_thread = threading.Thread(target=ngrok_start)
    ngrok_thread.start()
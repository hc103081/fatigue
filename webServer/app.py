import eventlet
eventlet.monkey_patch()

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
CORS(app, origins=["https://hc103081.github.io"])
socketio = SocketIO(app, cors_allowed_origins="*")  # 支援 WebSocket

# 全域變數緩存最新資料
latest_dataClass = None
latest_image_base64 = None

@app.route('/get_dataClass', methods=['GET'])
def get_dataClass():
    if latest_dataClass is None:
        return jsonify({"success": False, "error": "No dataClass available"})
    return jsonify({"success": True, "data": latest_dataClass})

@app.route('/get_latest_image', methods=['GET'])
def get_latest_image():
    if latest_image_base64 is None:
        return jsonify({"success": False, "error": "No image available"})
    return jsonify({"success": True, "image": latest_image_base64})

# WebSocket: Pi 端推送資料
@socketio.on('dataClass_update')
def handle_upload_dataClass(data):
    global latest_dataClass
    latest_dataClass = data
    emit('dataClass_update', data, broadcast=True)  # 廣播給前端

@socketio.on('image_update')
def handle_upload_image(data):
    global latest_image_base64
    latest_image_base64 = data
    emit('image_update', data, broadcast=True)  # 廣播給前端

# 保留原有 MJPEG 影像串流代理
@app.route('/video_feed', methods=['GET'])
def video_feed():
    pi_video_url = "https://undenunciated-ultrared-neil.ngrok-free.app/video_feed"
    try:
        import requests
        pi_response = requests.get(pi_video_url, stream=True, timeout=60)
        def generate():
            for chunk in pi_response.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk
        return app.response_class(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        return f"串流取得失敗: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # 用 eventlet.wsgi.server 啟動
    import eventlet.wsgi
    eventlet.wsgi.server(eventlet.listen(('', port)), app)
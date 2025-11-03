from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import base64

app = Flask(__name__)
CORS(app, origins=["https://hc103081.github.io"])
socketio = SocketIO(app, cors_allowed_origins="*")

latest_image_base64 = None
latest_dataClass = None

# WebSocket: Pi 端推送統一資料
@socketio.on('upload_dataClass')
def handle_upload_dataClass(data):
    global latest_dataClass
    latest_dataClass = data
    emit('dataClass_update', data, broadcast=True)

# WebSocket: Pi 端推送影像
@socketio.on('upload_image')
def handle_upload_image(img_base64):
    global latest_image_base64
    latest_image_base64 = img_base64
    emit('image_update', img_base64, broadcast=True)

# REST API: 取得最新統一資料（兼容前端輪詢）
@app.route('/get_dataClass', methods=['GET'])
def get_dataClass():
    global latest_dataClass
    if latest_dataClass is None:
        return jsonify({"success": False, "error": "No dataClass available"}), 404
    return jsonify({"success": True, "data": latest_dataClass})

# REST API: 取得最新影像（兼容前端輪詢）
@app.route('/get_latest_image', methods=['GET'])
def get_latest_image():
    global latest_image_base64
    if latest_image_base64:
        return jsonify({"success": True, "image_base64": latest_image_base64})
    else:
        return jsonify({"success": False, "error": "No image available"}), 404

# REST API: Pi 端 POST 推送資料（兼容舊版）
@app.route('/upload_dataClass', methods=['POST'])
def upload_dataClass():
    global latest_dataClass
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No dataClass provided"}), 400
        latest_dataClass = data
        socketio.emit('dataClass_update', data, broadcast=True)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# REST API: Pi 端 POST 推送影像（兼容舊版）
@app.route('/upload_image', methods=['POST'])
def upload_image():
    global latest_image_base64
    try:
        data = request.get_json()
        latest_image_base64 = data.get('image_base64')
        socketio.emit('image_update', latest_image_base64, broadcast=True)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
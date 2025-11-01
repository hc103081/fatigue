from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app, origins=["https://hc103081.github.io"])  # 新增這行

latest_image_base64 = None
latest_dataClass = None  # 新增快取 dataclass 統一資料


@app.route('/upload_dataClass', methods=['POST'])
def upload_dataClass():
    global latest_dataClass
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No dataClass provided"}), 400
        latest_dataClass = data
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/get_dataClass', methods=['GET'])
def get_dataClass():
    global latest_dataClass
    if latest_dataClass is None:
        return jsonify({"success": False, "error": "No dataClass available"}), 404
    return jsonify({"success": True, "data": latest_dataClass})


@app.route('/upload_image', methods=['POST'])
def upload_image():
    global latest_image_base64
    try:
        # Pi 端推送 base64 編碼的圖片
        data = request.get_json()
        latest_image_base64 = data.get('image_base64')
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/get_latest_image', methods=['GET'])
def get_latest_image():
    global latest_image_base64
    if latest_image_base64:
        return jsonify({"success": True, "image_base64": latest_image_base64})
    else:
        return jsonify({"success": False, "error": "No image available"}), 404



if __name__ == '__main__':
    app.run(threaded=True)

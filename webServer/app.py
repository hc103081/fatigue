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
        # Pi 端推送 dataclass 統一資料
        data = request.get_json()
        latest_dataClass = data.get('data')  # 建議 Pi 端 json 格式為 {"data": {...}}
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/get_dataClass', methods=['GET'])
def get_classdata():
    global latest_dataClass
    if latest_dataClass:
        return jsonify({
            "success": True,
            "data": latest_dataClass
        })
    else:
        return jsonify({
            "success": False,
            "error": "No dataClass available"
        }), 404

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

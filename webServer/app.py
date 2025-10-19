from flask import Flask, jsonify
import requests
from program.dataClass import SensorData
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://hc103081.github.io"])  # 新增這行


@app.route('/get_dataClass', methods=['GET', 'POST'])
def get_classdata():
    # 向 Pi 端請求最新資料
    pi_url = "https://undenunciated-ultrared-neil.ngrok-free.app/get_dataClass"
    try:
        pi_response = requests.get(pi_url, timeout=3)
        pi_data = pi_response.json()
        return jsonify(pi_data)
    except Exception as e:
        # 回傳明確的錯誤訊息
        return jsonify({
            "error": "樹莓派不在線",
            "detail": str(e)
        }), 500

if __name__ == '__main__':
    app.run()
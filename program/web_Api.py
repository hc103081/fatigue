from dataclasses import asdict
from flask import Flask, jsonify
from logs import Log
from dataClass import SensorData

app = Flask(__name__)

@app.route('/get_dataClass', methods=['GET'])
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

if __name__ == "__main__":
    app.run()
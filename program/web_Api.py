from dataclasses import asdict
import cv2
from flask import Flask, Response, jsonify
from .logs import Log
from .dataClass import DataUnified, ClassUnified

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
        try:
            data = self.unified.data
            if data is None:
                return jsonify({"success": False,
                                "error": "data is None"}), 500
            else:
                return jsonify({"success": True,
                                "data": asdict(data)})
        except Exception as e:
            Log.logger.warning(f"web get_dataClass error: {e}")
            return jsonify({"success": False,
                            "error": str(e)}), 500
    
    def video_feed(self):
        try:
            return Response(self.get_frame_encoded(), mimetype='multipart/x-mixed-replace; boundary=frame')
        except Exception as e:
            Log.logger.warning(f"video_feed error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500
        
    def get_frame_encoded(self):
        while True:
            try:
                frame = self.unified.camera.get_frame()
                if frame is None:
                    Log.logger.warning("未取得影像 frame，結束串流")
                    break
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    Log.logger.warning("影像編碼失敗")
                    continue
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                Log.logger.warning(f"串流錯誤: {e}")
                break
            
    def run(self):
        """
        啟動 Web API 伺服器
        """
        self.app.run(threaded=True)
    
if __name__ == "__main__":
    pass
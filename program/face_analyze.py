import time
from camera import Camera
from logs import Log
import dlib
import numpy as np
import cv2

class FaceAnalyzer(Camera):
    """臉部分析模組"""
    
    def __init__(self, camera_index=0):
        """
        初始化臉部分析器
        """
        super().__init__(camera_index)
        
        # 載入 dlib 的臉部偵測器與關鍵點預測模型
        self.detector = dlib.get_frontal_face_detector()
        
        # 需下載此模型
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks_GTX.dat") 
        
        # 記錄日志的時間間隔，單位：秒
        self.log_interval = 10  
        
        # 疲勞值
        self.fatigue_score = 0.0
        
        # 眼睛縱橫比 EAR
        self.ear = 0.0
        
        # 嘴巴張開比 MAR
        self.mar = 0.0
        

    def show(self):
        """
        顯示影像
        """
        frame = self.get_frame()
        if frame is None:
            Log.logger.warning("未取得影像 frame，跳過顯示")
            return
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        equa = cv2.equalizeHist(gray)
        face_rects = self.detector(equa,0)
        

        # 取出所有偵測的結果
        for i, d in enumerate(face_rects):
            x1 = d.left()
            y1 = d.top()
            x2 = d.right()
            y2 = d.bottom()

            # 以方框標示偵測的人臉
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4, cv2.LINE_AA)

        # 顯示結果
        cv2.imshow("Face Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass
            
    def update(self):
        """
        更新影像分析數據
        """
        frame = self.get_frame()
        if frame is None:
            now = time.time()
             
            # 只在超過 log_interval 秒才記錄
            if now - self.last_log_time > self.log_interval:  
                Log.logger.warning("未取得影像 frame，跳過分析")
                self.last_log_time = now
            return False
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        equa = cv2.equalizeHist(gray)
        faces = self.detector(equa)
        
        for face in faces:
            shape = self.predictor(equa, face)
            self.set_landmarks_points(shape)
            score = self.get_fatigue_score()
            fatigue = self.is_fatigued()
            
            # 畫左眼 (特徵點 36–41)
            for i in range(36, 42):
                x, y = shape.part(i).x, shape.part(i).y
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # 畫右眼 (特徵點 42–47)
            for i in range(42, 48):
                x, y = shape.part(i).x, shape.part(i).y
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # 畫嘴巴 (特徵點 48–67)
            for i in range(48, 68):
                x, y = shape.part(i).x, shape.part(i).y
                cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

            # 顯示結果W
            text = f"Fatigue Score: {score:.2f} | Fatigued: {fatigue}"
            cv2.putText(frame, text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255) if fatigue else (0, 255, 0), 2)
        cv2.imshow("Fatigue Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass
        return True
    
   # 計算眼睛縱橫比 EAR
    def compute_ear(self,eye_points):
        A = np.linalg.norm(eye_points[1] - eye_points[5])
        B = np.linalg.norm(eye_points[2] - eye_points[4])
        C = np.linalg.norm(eye_points[0] - eye_points[3])
        ear = (A + B) / (2.0 * C)
        return ear

    # 計算嘴巴張開比 MAR
    def compute_mar(self,mouth_points):
        A = np.linalg.norm(mouth_points[13] - mouth_points[19])  # 上下
        B = np.linalg.norm(mouth_points[14] - mouth_points[18])
        C = np.linalg.norm(mouth_points[12] - mouth_points[16])  # 左右
        mar = (A + B) / (2.0 * C)
        return mar

    def set_landmarks_points(self,landmarks):
        left_eye = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(36, 42)])
        right_eye = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(42, 48)])
        mouth = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(48, 68)])

        self.ear = (self.compute_ear(left_eye) + self.compute_ear(right_eye)) / 2.0
        self.mar = self.compute_mar(mouth)
        return left_eye, right_eye, mouth

    # 回傳疲勞值（EAR 越低 + MAR 越高 → 疲勞越高）
    def get_fatigue_score(self):
        # 疲勞值公式：MAR - EAR（可依需求調整權重）
        fatigue_score = self.mar - self.ear
        self.fatigue_score = fatigue_score
        return fatigue_score

    # 回傳是否疲勞（根據疲勞值是否超過閾值）
    def is_fatigued(self, threshold=0):
        self.fatigue_score = self.get_fatigue_score()
        return (self.fatigue_score > threshold)
        
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        pass
from dataclasses import dataclass
import time
from camera import Camera
from logs import Log
import dlib
import numpy as np
import cv2

class FaceAnalyzer(Camera):
    """臉部分析模組"""
    
    @dataclass
    class FatigueData:
        fatigue_score: float    # 疲勞值
        is_fatigued: bool       # 是否疲勞
        ear: float              # 眼睛縱橫比
        mar: float              # 嘴巴開合比
        threshold: float        # 疲勞閾值
    
    def __init__(self, camera_index=0, threshold=0.3):
        """
        初始化臉部分析器
        Params:
            camera_index: 攝影機索引
            threshold: 疲勞閾值
        """
        self.data = FaceAnalyzer.FatigueData(
            fatigue_score=0.0,
            is_fatigued=False,
            ear=0.0,
            mar=0.0,
            threshold=threshold
        )
        
        super().__init__(camera_index)
        
        # 載入 dlib 的臉部偵測器與關鍵點預測模型
        self.detector = dlib.get_frontal_face_detector()
        
        # 需下載此模型
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks_GTX.dat") 
        
        # 記錄日志的時間間隔，單位：秒
        self.log_interval = 10  

    def get_data(self):
        """
        取得臉部分析數據
        Returns:
            FaceAnalyzer.FatigueData: 臉部分析數據
        """
        data = FaceAnalyzer.FatigueData(
            fatigue_score=self.get_fatigue_score(),
            is_fatigued=self.is_fatigued(),
            ear=self.data.ear,
            mar=self.data.mar,
            threshold=self.data.threshold
        )
        return data

    def update(self,show=False):
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
        gray = cv2.equalizeHist(gray)
        faces = self.detector(gray)
        
        for face in faces:
            # 提取臉部關鍵點
            landmarks = self.predictor(gray, face)
            
            # 提取眼睛縱橫比和嘴巴開合比
            self.data.ear,self.data.mar = self.get_ear_mar(landmarks)
            # 計算疲勞值
            self.data.fatigue_score = self.get_fatigue_score()
            self.data.is_fatigued = self.is_fatigued()
            
            # 顯示臉部關鍵點
            if show:
                self.show(frame,landmarks)
        
        return True

    def show(self,frame,landmarks):
        """
        顯示影像
        """
        if frame is None:
            Log.logger.warning("未取得影像 frame，跳過顯示")
            return

        # 畫左眼 (特徵點 36–41)
        for i in range(36, 42):
            x, y = landmarks.part(i).x, landmarks.part(i).y
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        # 畫右眼 (特徵點 42–47)
        for i in range(42, 48):
            x, y = landmarks.part(i).x, landmarks.part(i).y
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        # 畫嘴巴 (特徵點 48–67)
        for i in range(48, 68):
            x, y = landmarks.part(i).x, landmarks.part(i).y
            cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

        # 顯示結果W
        text = f"Fatigue Score: {self.data.fatigue_score:.2f} | Fatigued: {self.data.is_fatigued}"
        cv2.putText(frame, text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255) if self.data.is_fatigued else (0, 255, 0), 2)
            
        
        # 顯示結果
        cv2.imshow("Face Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass
            
    
    def compute_ear(self,eye_points):
        """
        計算眼睛縱橫比 EAR
        """
        A = np.linalg.norm(eye_points[1] - eye_points[5])
        B = np.linalg.norm(eye_points[2] - eye_points[4])
        C = np.linalg.norm(eye_points[0] - eye_points[3])
        ear = (A + B) / (2.0 * C)
        return ear

    def compute_mar(self,mouth_points):
        """
        計算嘴巴張開比 MAR
        """
        A = np.linalg.norm(mouth_points[13] - mouth_points[19])  # 上下
        B = np.linalg.norm(mouth_points[14] - mouth_points[18])
        C = np.linalg.norm(mouth_points[12] - mouth_points[16])  # 左右
        mar = (A + B) / (2.0 * C)
        return mar

    def get_ear_mar(self,landmarks):
        """
        計算眼睛縱橫比 EAR 與嘴巴張開比 MAR
        """
        left_eye = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(36, 42)])
        right_eye = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(42, 48)])
        mouth = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(48, 68)])

        ear = (self.compute_ear(left_eye) + self.compute_ear(right_eye)) / 2.0
        mar = self.compute_mar(mouth)
        return ear,mar

    def get_fatigue_score(self):
        """
        回傳疲勞值（EAR 越低 + MAR 越高 → 疲勞越高）
        """
        # 疲勞值公式：MAR - EAR（可依需求調整權重）
        fatigue_score = self.data.mar - self.data.ear
        return fatigue_score
    
    def set_threshold(self,threshold):
        """
        設定疲勞值閾值
        Params:
            threshold: 疲勞值閾值
        """
        self.data.threshold = threshold

    def is_fatigued(self):
        """
        回傳是否疲勞（根據疲勞值是否超過閾值）
        Params:
            threshold: 疲勞值閾值
        Returns:
            如果疲勞值超過 threshold 則回傳 True
        """
        return (self.get_fatigue_score() > self.data.threshold)
        
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
from camera import Camera
from logs import Log
import dlib
import numpy as np

class FaceAnalyzer(Camera):
    """臉部分析模組"""
    
    def __init__(self):
        """
        初始化臉部分析器
        """
        super().__init__()
        
        # 載入 dlib 的臉部偵測器與關鍵點預測模型
        self.detector = dlib.get_frontal_face_detector()
        
        # 需下載此模型
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks_GTX.dat") 

            
    def update(self):
        """
        更新影像分析數據
        """
        pass
    
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

    # 回傳疲勞值（EAR 越低 + MAR 越高 → 疲勞越高）
    def get_fatigue_score(self,landmarks):
        left_eye = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(36, 42)])
        right_eye = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(42, 48)])
        mouth = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(48, 68)])

        ear = (self.compute_ear(left_eye) + self.compute_ear(right_eye)) / 2.0
        mar = self.compute_mar(mouth)

        # 疲勞值公式：MAR - EAR（可依需求調整權重）
        fatigue_score = mar - ear
        
        return fatigue_score

    # 回傳是否疲勞（根據疲勞值是否超過閾值）
    def is_fatigued(self,fatigue_score, threshold=0):
        return (fatigue_score > threshold)
        
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        pass
    
    
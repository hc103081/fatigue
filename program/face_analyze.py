from dataclasses import dataclass
import os
import time
from .logs import Log
from .camera import Camera
import numpy as np
import cv2
import google.generativeai as genai
import mediapipe as mp
import collections
import threading
from PIL import Image
import io

class FaceAnalyzer():
    """臉部分析模組"""
    
    @dataclass
    class FatigueData():
        fatigue_score: float    # 疲勞值
        is_fatigued: bool       # 是否疲勞
        ear: float              # 眼睛縱橫比
        mar: float              # 嘴巴開合比
        threshold: float        # 疲勞閾值
    
    def __init__(self, camera: Camera, use_mock=False, threshold=0.3):
        """
        初始化臉部分析器
        Params:
            camera: 攝影機物件
            use_mock: 是否使用模擬資料
            threshold: 疲勞閾值
        """
        self.camera = camera
        self.data = FaceAnalyzer.FatigueData(
            fatigue_score=0.0,
            is_fatigued=False,
            ear=0.0,
            mar=0.0,
            threshold=threshold
        )
        
        # 初始化 MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

        # 初始化 GenAI
        genai.configure(api_key=os.getenv("GENAI_API_KEY"))
        self.genai = genai.GenerativeModel("gemini-2.5-flash")

        # 影像幀緩衝區
        self.frame_buffer = collections.deque(maxlen=60)
        # 閉眼計數器
        self.closed_eyes_counter = 0
        # 上次觸發時間
        self.last_trigger_time = 0
        # 冷卻時間 (秒)
        self.cooldown_period = 60

        # GenAI 分析結果
        self.last_genai_response = None

        # 是否使用模擬資料
        self.is_test_data = use_mock
        
        # 記錄日志的時間間隔，單位：秒
        self.log_interval = 10  
        
        self.last_log_time = time.time()


    def get_data(self) -> FatigueData:
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
            threshold=self.data.threshold,
        )
        return data

    def update(self,show=False) -> bool:
        """
        更新影像分析數據
        Params:
            show: 是否顯示分析結果
        Returns:
            True: 成功更新
            False: 失敗更新
        """
        # 使用模擬資料
        if self.is_test_data:
            import random
            self.data.ear = round(random.uniform(0.2, 0.3), 3)
            self.data.mar = round(random.uniform(0.3, 0.6), 3)
            self.data.fatigue_score = self.get_fatigue_score()
            self.data.is_fatigued = self.is_fatigued()
            return True
        
        # 從攝像頭獲取影像幀
        frame = self.camera.get_frame()
        if frame is None:
            now = time.time()
             
            # 只在超過 log_interval 秒才記錄
            if now - self.last_log_time > self.log_interval:  
                Log.logger.warning("未取得影像 frame，跳過分析")
                self.last_log_time = now
            return False

        # 將 frame 加入緩衝區
        self.frame_buffer.append(frame)

        # 將影像從 BGR 轉換為 RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = self.face_mesh.process(image_rgb)
        image_rgb.flags.writeable = True
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # 提取眼睛縱橫比和嘴巴開合比
                self.data.ear, self.data.mar = self.get_ear_mar(face_landmarks, frame.shape[1], frame.shape[0])
                # 計算疲勞值
                self.data.fatigue_score = self.get_fatigue_score()
                self.data.is_fatigued = self.is_fatigued()

                # 檢查是否閉眼
                if self.data.ear < 0.2:
                    self.closed_eyes_counter += 1
                else:
                    self.closed_eyes_counter = 0

                # 檢查是否觸發疲勞事件
                current_time = time.time()
                if self.closed_eyes_counter >= 15 and (current_time - self.last_trigger_time) > self.cooldown_period:
                    self.last_trigger_time = current_time
                    # 在新執行緒中觸發疲勞事件，避免阻塞主執行緒
                    thread = threading.Thread(target=self._trigger_fatigue_action)
                    thread.start()

                # 顯示臉部關鍵點
                if show:
                    self.show(frame, face_landmarks)
                
        if show:
            # 顯示結果
            cv2.imshow("Face Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                return False
        
        return True

    def show(self,frame,landmarks) -> None:
        """
        顯示影像
        """
        if frame is None:
            Log.logger.warning("未取得影像 frame，跳過顯示")
            return

        # 使用 MediaPipe 的繪圖工具繪製臉部網格
        self.mp_drawing.draw_landmarks(
            image=frame,
            landmark_list=landmarks,
            connections=self.mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=self.drawing_spec,
            connection_drawing_spec=self.drawing_spec)

        # 顯示結果W
        text = f"Fatigue Score: {self.data.fatigue_score:.2f} | Fatigued: {self.data.is_fatigued}"
        cv2.putText(frame, text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255) if self.data.is_fatigued else (0, 255, 0), 2)
        
            
    
    def compute_ear(self,eye_points) -> float:
        """
        計算眼睛縱橫比 EAR
        """
        A = np.linalg.norm(eye_points[1] - eye_points[5])
        B = np.linalg.norm(eye_points[2] - eye_points[4])
        C = np.linalg.norm(eye_points[0] - eye_points[3])
        ear = (A + B) / (2.0 * C)
        return ear

    def compute_mar(self,mouth_points) -> float:
        """
        計算嘴巴張開比 MAR
        """
        # 使用內唇垂直距離與嘴角水平距離計算
        inner_lip_vertical_dist = np.linalg.norm(mouth_points[4] - mouth_points[5])
        mouth_width = np.linalg.norm(mouth_points[0] - mouth_points[1])
        
        # 避免除以零
        if mouth_width == 0:
            return 0.0
            
        mar = inner_lip_vertical_dist / mouth_width
        return mar

    def get_ear_mar(self,landmarks, img_w, img_h) -> tuple:
        """
        計算眼睛縱橫比 EAR 與嘴巴張開比 MAR
        """
        # 將正規化座標轉換為像素座標
        landmark_points = np.array([[lm.x * img_w, lm.y * img_h] for lm in landmarks.landmark])

        # MediaPipe 的眼睛與嘴巴特徵點索引
        # 參考: https://github.com/google/mediapipe/blob/master/mediapipe/modules/face_geometry/data/canonical_face_model_uv_visualization.png
        LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
        RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
        # [嘴角左, 嘴角右, 上唇頂, 下唇底, 內上唇, 內下唇]
        MOUTH_INDICES = [61, 291, 0, 17, 13, 14]

        # 提取眼睛和嘴巴的特徵點
        left_eye_points = landmark_points[LEFT_EYE_INDICES]
        right_eye_points = landmark_points[RIGHT_EYE_INDICES]
        mouth_points = landmark_points[MOUTH_INDICES]

        # 計算 EAR 和 MAR
        ear = (self.compute_ear(left_eye_points) + self.compute_ear(right_eye_points)) / 2.0
        mar = self.compute_mar(mouth_points)
        return ear,mar

    def get_fatigue_score(self) -> float:
        """
        回傳疲勞值（EAR 越低 + MAR 越高 → 疲勞越高）
        """
        # 疲勞值公式：MAR - EAR（可依需求調整權重）
        fatigue_score = self.data.mar - self.data.ear
        return fatigue_score
    
    def set_threshold(self,threshold) -> None:
        """
        設定疲勞值閾值
        Params:
            threshold: 疲勞值閾值
        """
        self.data.threshold = threshold

    def is_fatigued(self) -> bool:
        """
        回傳是否疲勞（根據疲勞值是否超過閾值）
        Params:
            threshold: 疲勞值閾值
        Returns:
            如果疲勞值超過 threshold 則回傳 True
        """
        return (self.get_fatigue_score() > self.data.threshold)

    def get_genai_response(self) -> str | None:
        """
        取得最新的 GenAI 分析結果，如果沒有新結果則回傳 None
        """
        response = self.last_genai_response
        Log.logger.info(f"取得 GenAI 回應: {response}")
        self.last_genai_response = None # 讀取後清除
        return response

    def _trigger_fatigue_action(self):
        """
        觸發疲勞事件，組合過去、過渡、現在的影像並上傳至 GenAI 分析
        """
        if len(self.frame_buffer) < 45:
            Log.logger.warning("緩衝區影像幀不足，無法觸發疲勞事件")
            return

        # 從緩衝區中取得過去、過渡、現在的影像
        past_frame = self.frame_buffer[-45]
        transition_frame = self.frame_buffer[-10]
        now_frame = self.frame_buffer[-1]

        # 調整影像大小並合併
        past_frame_resized = cv2.resize(past_frame, (320, 240))
        transition_frame_resized = cv2.resize(transition_frame, (320, 240))
        now_frame_resized = cv2.resize(now_frame, (320, 240))
        stitched_image = cv2.hconcat([past_frame_resized, transition_frame_resized, now_frame_resized])

        # 上傳至 GenAI 分析並儲存結果
        self.last_genai_response = self.upload_fatigue_image_to_genai(
            stitched_image,
            ear=self.data.ear,
            mar=self.data.mar,
            fatigue_score=self.data.fatigue_score
        )

    def upload_fatigue_image_to_genai(self, image: np.ndarray, ear: float, mar: float, fatigue_score: float) -> str | None:
        """
        將影像上傳至 GenAI 進行疲勞分析
        Params:
            image: 要上傳的影像 (NumPy array)
            ear: 眼睛縱橫比 (Eye Aspect Ratio)
            mar: 嘴巴開合比 (Mouth Aspect Ratio)
            fatigue_score: 系統計算的疲勞分數
        Returns:
            GenAI 的分析結果 JSON 字串，或在失敗時回傳 None
        """
        try:
            # 將 OpenCV 影像 (NumPy array) 轉換為 PIL Image
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image_rgb)

            # 準備上傳的內容 (僅保留專業版 JSON 格式)
            prompt = f"""
請根據這張組合圖片與數據，用台灣人習慣的繁體中文，生成一份專業的疲勞分析報告。

**數據:**
- 眼睛縱橫比 (EAR): {ear:.2f}
- 嘴巴開合比 (MAR): {mar:.2f}
- 系統疲勞分數: {fatigue_score:.2f}

**回傳格式 (請嚴格遵守 JSON 格式，不要包含任何 ```json ``` 標籤):**
{{
  "summary": "在這裡簡短敘述重點，約 20-30 字。",
  "analysis": "在這裡提供詳細的視覺分析，說明您判斷的依據，例如眼睛狀態、嘴巴狀態、面部表情等。",
  "conclusion": "在這裡給出明確的結論，例如『綜合判斷，人物處於高度疲勞狀態』。",
  "suggestion": "在這裡提供具體的建議，例如『建議立即停車休息 15 分鐘』或『狀態良好，可繼續駕駛』。"
}}
"""
            
            Log.logger.info("正在上傳影像至 GenAI 進行分析...")
            
            # 使用 GenAI 進行分析
            response = self.genai.generate_content([prompt, pil_image])
            
            # 記錄 GenAI 的分析結果
            if response and response.text:
                Log.logger.info(f"GenAI 分析結果: {response.text}")
                return response.text
            else:
                Log.logger.warning("GenAI 未回傳有效的分析結果")
                return None

        except Exception as e:
            Log.logger.error(f"上傳影像至 GenAI 失敗: {e}")
            return None
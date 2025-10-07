from camera import Camera

class FaceAnalyzer:
    
    def __init__(self, model_path=None):
        self.model = None
        if model_path:
            self.load_model(model_path)

    def load_model(self, model_path):
        # 載入AI模型的接口
        # 這裡假設使用某個深度學習框架，例如TensorFlow或PyTorch
        # 例如: self.model = tf.keras.models.load_model(model_path)
        pass

    def analyze(self,image):
        """
        分析臉部疲勞
        Params:
            image: 圖片
        """
        if self.model is None:
            raise ValueError("Model not loaded.")
        # result = self.model.predict(image)
        # return result
        pass
    
    # 臉部疲勞分析指標
    def get_fatigue(self):
        """
        取得臉部疲勞值
        """
        result = self.analyze()
        
        return result
    
    def is_fatigue(self):
        """
        判斷臉部疲勞
        """
        fatigue_value = self.get_fatigue()
        
        return fatigue_value > 0.15
        

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    
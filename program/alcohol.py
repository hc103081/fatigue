import random
from logs import Log

class AlcoholSensor:
    """
    酒精感測器模組
    """
    def __init__(self, sensor_id):
        """
        Params:
            sensor_id: 感測器ID
        """
        self.sensor_id = sensor_id
        self.alcohol_level = 0.0

    def update(self):
        """
        更新感測器資料
        """
        return True
    
    # 取得模擬的酒精濃度值
    def get_alcohol(self):
        """ 
        Returns:
            回傳模擬的酒精濃度值
        """
        self.alcohol_level = round(random.uniform(0.0, 0.1), 3)
        return self.alcohol_level

    # 判斷酒精濃度是否超過限制值
    def is_over_limit(self, limit=0.15):
        """
        Params:
            limit: 酒精濃度限制值
        Returns:
            如果酒精濃度超過 limit 則回傳 True
        """
        return self.alcohol_level > limit

    # 重置酒精濃度值
    def reset(self):
        """ 重置酒精濃度值 """
        self.alcohol_level = 0.0
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
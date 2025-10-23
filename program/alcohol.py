from dataclasses import dataclass
import random
from logs import Log

class AlcoholSensor:
    """
    酒精感測器模組
    """
    @dataclass
    class AlcoholData:
        alcohol_value: float  # 酒精濃度值
        is_over_limit: bool   # 是否超過濃度限制
        is_test_data: bool    # 新增，根據 use_mock 判斷是否為測試資料
        limit: float          # 酒精濃度限制值
    
    def __init__(self, use_mock=False, limit=0.15):
        """
        Params:
            use_mock: 是否使用模擬資料
            limit: 酒精濃度限制值
        """
        self.data = AlcoholSensor.AlcoholData(
            alcohol_value=0.0,
            is_over_limit=False,
            is_test_data=use_mock,
            limit=limit
        )
        
        self.use_mock = use_mock

    def update(self):
        """
        更新感測器資料
        """
        if self.use_mock:
            self.data.alcohol_value = round(random.uniform(0.0, 0.2), 3)
        else:
            # 這裡放真實感測器資料刷新邏輯
            pass
        return True
    
    def get_data(self):
        """
        Returns:
            回傳酒精感測器資料
        """
        data = AlcoholSensor.AlcoholData(
            alcohol_value=self.get_alcohol(),
            is_over_limit=self.is_over_limit(),
            is_test_data=self.data.is_test_data,
            limit=self.data.limit
        )
        return data
    
    def get_alcohol(self):
        """ 
        Returns:
            回傳模擬的酒精濃度值
        """
        return self.data.alcohol_value

    def is_over_limit(self):
        """
        Params:
            limit: 酒精濃度限制值
        Returns:
            如果酒精濃度超過 limit 則回傳 True
        """
        return self.data.alcohol_value > self.data.limit

    def reset(self):
        """ 重置酒精濃度值 """
        self.data.alcohol_value = 0.0
        
    def set_limit(self, limit: float):
        """
        設定酒精濃度限制值
        Params:
            limit: 新的酒精濃度限制值
        """
        self.data.limit = limit
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
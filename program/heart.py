from dataclasses import dataclass
from queue import Queue
from .logs import Log


class HeartRateSensor:
    """
    用於管理心率感測器的讀數，並提供新增、查詢、計算平均值及判斷異常等功能。
    """
    @dataclass
    class HeartData:
        bpm_latest: int             # 最新一次的心率讀數
        bpm_average: float           # 心率讀數的平均值
        is_heart_rate_normal: bool   # 心率是否正常
        queue_size: int              # 用於存儲心率讀數的隊列大小
        threshold_low: int           # 心率異常判斷的下限值
        threshold_high: int          # 心率異常判斷的上限值
        is_test_data: bool = False   # 是否為測試數據，用於模擬心率讀數

    def __init__(self, use_mock=False, threshold_low=60, threshold_high=100):
        """
        HeartRateSensor 類用於管理心率感測器的讀數，並提供新增、查詢、計算平均值及判斷異常等功能。\n
        bpm: 心率讀數（每分鐘心跳次數），用於 add_reading 方法。\n
        threshold_low: 心率異常判斷的下限值\n
        threshold_high: 心率異常判斷的上限值
        Params:
            use_mock: 是否使用模擬資料
            threshold_low: 心率異常判斷的下限值
            threshold_high: 心率異常判斷的上限值
        """
        self.data = self.HeartData(
            bpm_latest=0,
            bpm_average=0.0,
            is_heart_rate_normal=True,
            queue_size=10,
            threshold_low=threshold_low,
            threshold_high=threshold_high,
            is_test_data=use_mock
        )
        self.use_mock = use_mock   # 是否使用模擬資料
        self.heart_queue = Queue() # 用於存儲心率讀數的隊列

    def update(self):
        """
        刷新心率感測器資料。
        """
        if self.use_mock:
            import random
            mock_bpm = random.randint(70, 110)
            self.add_reading(mock_bpm)
        else:
            # 這裡放真實感測器資料刷新邏輯
            pass
        return True
    
    def get_data(self):
        """
        Returns:
            回傳心率感測器資料
        """
        data = HeartRateSensor.HeartData(
            bpm_latest=self.get_latest(),
            bpm_average=self.get_average(),
            is_heart_rate_normal=self.is_normal(),
            queue_size=self.data.queue_size,
            threshold_low=self.data.threshold_low,
            threshold_high=self.data.threshold_high,
            is_test_data=self.data.is_test_data
        )
        return data
    
    # 新增一次心率讀數
    def add_reading(self, bpm):
        """
        @param bpm: 新增一次心率讀數（bpm）
        """
        if self.heart_queue.full():
            self.heart_queue.get()
        self.heart_queue.put(bpm)
        
    # 取得最新一次的心率讀數
    def get_latest(self):
        """
        Returns:
            回傳最新一次的心率讀數
        """
        return self.heart_queue.queue[-1] if not self.heart_queue.empty() else 0

    # 取得所有心率讀數的平均值
    def get_average(self):
        """
        Returns:
            回傳所有心率讀數的平均值
        """
        return sum(self.heart_queue.queue) / len(self.heart_queue.queue) if not self.heart_queue.empty() else 0
    # 判斷是否有異常
    def is_normal(self):
        """
        Params:
            threshold_low: 心率異常判斷的下限值
            threshold_high: 心率異常判斷的上限值
        Returns:
            如果最新一次的心率讀數低於 threshold_low 或
            高於 threshold_high 就回傳 False
        """
        # 取得最新一次的心率讀數
        average = self.get_average()
        if average == 0:
            return False
        return average < self.data.threshold_low or average > self.data.threshold_high
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
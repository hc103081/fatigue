from queue import Queue
from logs import Log


class HeartRateSensor:
    
    def __init__(self):
        """
        HeartRateSensor 類用於管理心率感測器的讀數，並提供新增、查詢、計算平均值及判斷異常等功能。\n
        bpm: 心率讀數（每分鐘心跳次數），用於 add_reading 方法。\n
        threshold_low: 心率異常判斷的下限值，預設為 60。\n
        threshold_high: 心率異常判斷的上限值，預設為 100。
        """
        self.data = Queue(30)
        self.threshold_now = 60

    def update(self):
        """
        刷新心率感測器資料。
        """
        pass
    
    # 新增一次心率讀數
    def add_reading(self, bpm):
        """
        @param bpm: 新增一次心率讀數（bpm）
        """
        if self.data.full():
            self.data.get()
            self.data.put(bpm)
        else:
            self.data.put(bpm)
        self.threshold_now = bpm
        
    # 取得最新一次的心率讀數
    def get_latest(self):
        """
        Returns:
            回傳最新一次的心率讀數
        """
        return self.threshold_now

    # 取得所有心率讀數的平均值
    def get_average(self):
        """
        Returns:
            回傳所有心率讀數的平均值
        """
        return sum(self.data.queue) / len(self.data.queue) if len(self.data.queue) > 0 else None

    # 判斷是否有異常
    def is_normal(self, threshold_low=60, threshold_high=100):
        """
        Params:
            threshold_low: 心率異常判斷的下限值，預設為 60。\n
            threshold_high: 心率異常判斷的上限值，預設為 100。
        Returns:
            如果最新一次的心率讀數低於 threshold_low 或
            高於 threshold_high 則回傳 True
        """
        # 取得最新一次的心率讀數
        average = self.get_average()
        if average is None:
            return False
        return average < threshold_low or average > threshold_high
    
    
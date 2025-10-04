class GPIO:
    """
    Params:
        BCM: GPIO.BCM
        OUT: GPIO.OUT
        HIGH: GPIO.HIGH
        LOW: GPIO.LOW
    """
    BCM = None  # BCM編號
    BOARD = None  # 板載編號
    OUT = None  # 輸出模式
    HIGH = 1    # 高態
    LOW = 0     # 低態
    PUD_UP = None  # 上拉電阻
    PUD_DOWN = None  # 下拉電阻

    @staticmethod
    def setmode(mode): pass

    @staticmethod
    def setup(pin, mode, pull_up_down=None): pass
    
    @staticmethod
    def input(pin): pass

    @staticmethod
    def output(pin, state): pass

    @staticmethod
    def cleanup(pin=None): pass
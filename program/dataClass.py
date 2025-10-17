from dataclasses import dataclass

@dataclass
class SensorData:
    alcohol_level: float = 0.0
    is_alcohol: bool = False
    heart_rate: int = 0
    is_heart_rate_normal: bool = True
    fatigue_score: float = 0.0
    is_fatigued: bool = False
    camera_ok: bool = True
    

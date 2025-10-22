from dataclasses import dataclass
from heart import HeartRateSensor
from alcohol import AlcoholSensor
from face_analyze import FaceAnalyzer

@dataclass
class DataUnified:
    alcohol: AlcoholSensor.AlcoholData
    heart: HeartRateSensor.HeartData
    fatigue: FaceAnalyzer.FatigueData

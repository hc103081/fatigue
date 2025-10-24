from __future__ import annotations
from dataclasses import dataclass

# program class
from .heart import HeartRateSensor
from .alcohol import AlcoholSensor
from .face_analyze import FaceAnalyzer
from .line_Api import Line_Api
from .ngrok import Ngrok
from .gpio import GPIO

@dataclass
class DataUnified:
    """
    整合感測器資料的類別
    """
    alcohol: AlcoholSensor.AlcoholData
    heart: HeartRateSensor.HeartData
    fatigue: FaceAnalyzer.FatigueData
    
@dataclass
class ClassUnified:
    """
    整合感測器類別的類別
    """
    data: DataUnified
    alcohol: AlcoholSensor
    heart: HeartRateSensor
    fatigue: FaceAnalyzer
    line_api: Line_Api
    
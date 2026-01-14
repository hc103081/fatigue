from dataclasses import dataclass

# program class
from .alcohol import AlcoholSensor
from .face_analyze import FaceAnalyzer
from .line_Api import Line_Api
from .camera import Camera

@dataclass
class DataUnified:
    """
    整合感測器資料的類別
    """
    alcohol: AlcoholSensor.AlcoholData
    fatigue: FaceAnalyzer.FatigueData
    
@dataclass
class ClassUnified:
    """
    整合感測器類別的類別
    """
    
    data: DataUnified = None
    alcohol: AlcoholSensor = None
    fatigue: FaceAnalyzer = None
    line_api: Line_Api = None
    camera: Camera = None
    
from dataclasses import dataclass
from __future__ import annotations


from heart import HeartRateSensor
from alcohol import AlcoholSensor
from face_analyze import FaceAnalyzer
from ui import FatigueMonitorUI
from line_Api import Line_Api
from line_bot import Line_bot
from gpio import GPIO
from ngrok import Ngrok
from web_Api import WebApi



@dataclass
class DataUnified:
    """
    整合感測器資料的類別
    """
    alcohol: AlcoholSensor.AlcoholData
    heart: HeartRateSensor.HeartData
    fatigue: FaceAnalyzer.FatigueData
    line: Line_Api.LineData
    
@dataclass
class ClassUnified:
    """
    整合感測器類別的類別
    """
    alcohol: AlcoholSensor
    heart: HeartRateSensor
    fatigue: FaceAnalyzer
    line_api: Line_Api
    line_bot: Line_bot
    gpio: GPIO
    web_api: WebApi
    ui: FatigueMonitorUI
    ngrok: Ngrok
    
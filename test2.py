from program import *

camera = Camera(camera_index=0,
                frame_width=640,
                frame_height=480)
face_analyzer = FaceAnalyzer(camera)

while True:

    face_analyzer.update(True)
    

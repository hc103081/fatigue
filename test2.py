from program import *

def face_test():

    camera = Camera(camera_index=0,
                    frame_width=640,
                    frame_height=480)
    face_analyzer = FaceAnalyzer(camera)

    while True:

        face_analyzer.update(True)
        
def max30102_test():
    from max30102 import MAX30102,HeartRateMonitor
    import time
    import argparse
    


    parser = argparse.ArgumentParser(description="Read and print data from MAX30102")
    parser.add_argument("-r", "--raw", action="store_true",
                        help="print raw data instead of calculation result")
    parser.add_argument("-t", "--time", type=int, default=30,
                        help="duration in seconds to read from sensor, default 30")
    parser.add_argument("-s", "--show", action="store_true",
                        help="show spo2 data using matplotlib")
    args = parser.parse_args()

    print('sensor starting...')
    hrm = HeartRateMonitor(print_raw=args.raw, print_result=(not args.raw))
    hrm.start_sensor()
    try:
        time.sleep(args.time)
    except KeyboardInterrupt:
        print('keyboard interrupt detected, exiting...')

    hrm.stop_sensor()

    if args.show:
        hrm.show()
    print('sensor stoped!')
def mq3_test_dout():
    import RPi.GPIO as GPIO
    import time
    
    DOUT_PIN = 17  # 依你的接線設定
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DOUT_PIN, GPIO.IN)
    
    while True:
        value = GPIO.input(DOUT_PIN)
        print("DOUT:", value)  # 0=低濃度, 1=高濃度（超過臨界值）
        time.sleep(1)
        
def  face_analyze_test2():
    from program import FaceAnalyzer
    import cv2
    import numpy as np  
    
        

    camera = Camera(camera_index=0,
                    frame_width=640,
                    frame_height=480)
    with FaceAnalyzer(camera) as face_analyzer:
        while True:
            face_analyzer.update(show=True)

        
if __name__ == "__main__":
    #max30102_test() 
    # face_test()
    # mq3_test_dout()
    face_analyze_test2()
    pass
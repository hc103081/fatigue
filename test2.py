import time
from program import *

line_api = Line_Api(
            {'Hong':'Uc588694833df79cafd6d19b3c2f505af',
            'Kai': 'U44a5e3e3cf9c8835a64bb1273b08f457'
            },
            access_token='ltwy2UPyvHTg7JAKyDWeRuQsF2wGkiGbe7zguLV9K6P5Gxbh8LyV8TgecpwefKmsVjDrv+pHqDIjzM2kuolIt2 Co2xQ0PLnIPdw57yuKJ9+l2L7xhrnZAKKHyX+PVhlUcMtJ1zokKK8/HoJpbzvLsQdB04t89/1O/w1cDnyilFU=',
            secret='ccb3a53029a0ae2eda6fd90ed07e4fd0',
            state_open=True,
        )  


def test_sent_message():
    """
    測試 Line_Api 的 sent_message 方法
    """
    user_id = line_api.data.user_id['Kai']
    message = input("請輸入測試訊息: ")
    result = line_api.message(message).sent(user_id)
    print(f"訊息傳送結果: {result}")

def mp3_test():
    """
    測試 MP3Player 播放功能
    """
    player = MP3Player()
    player.play("alcohol_warning", loops=0)
    
    player.play("fatigue_warning", loops=0)
    time.sleep(1)  # 等待 5 秒鐘    
    player.pause()
    time.sleep(4)  # 等待 5 秒鐘
    
    player.restart()
    
    
    print("正在播放音效...")
    while True:
        time.sleep(1)

def face_test():
    """
    測試 FaceAnalyzer 功能
    """
    camera = Camera(frame_width=640, frame_height=480)
    analyzer = FaceAnalyzer(camera=camera, use_mock=False)
    while True:
        analyzer.update(show=True)
        data = analyzer.get_data()
        print(f"疲勞分數: {data.fatigue_score}, 是否疲勞: {data.is_fatigued}", end='\r', flush=True)

        # 檢查是否有來自 GenAI 的新回應
        genai_response = analyzer.get_genai_response()
        if genai_response:
            print(f"收到 GenAI 回應: {genai_response}")
            # 發送 LINE 通知
            user_id = line_api.data.user_id['Hong']
            line_api.message(f"疲勞分析結果：\n{genai_response}").sent(user_id)

        time.sleep(0.03)  # 模擬每秒約 30 幀
        

if __name__ == "__main__":
    # line_api.open_sent_message()
    # test_sent_message()
    # mp3_test()
    face_test()
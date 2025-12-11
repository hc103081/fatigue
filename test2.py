from program import *

line_api = Line_Api(
            {'Hong':'Uc588694833df79cafd6d19b3c2f505af',
            'Kai': 'U44a5e3e3cf9c8835a64bb1273b08f457'
            },
            access_token='ltwy2UPyvHTg7JAKyDWeRuQsF2wGkiGbe7zguLV9K6P5Gxbh8LyV8TgecpwefKmsVjDrv+pHqDIjzM2kuolIt2 Co2xQ0PLnIPdw57yuKJ9+l2L7xhrnZAKKHyX+PVhlUcMtJ1zokKK8/HoJpbzvLsQdB04t89/1O/w1cDnyilFU=',
            secret='ccb3a53029a0ae2eda6fd90ed07e4fd0',
            state_open=True,
            status_can_sent_message=False
        )  


def test_sent_message():
    """
    測試 Line_Api 的 sent_message 方法
    """
    user_id = line_api.data.user_id['Kai']
    message = input("請輸入測試訊息: ")
    result = line_api.sent_message(user_id, message)
    print(f"訊息傳送結果: {result}")

if __name__ == "__main__":
    line_api.open_sent_message()
    test_sent_message()
    print("測試通過！")

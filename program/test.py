from line_bot import Line_bot
import RPi.GPIO as GPIO    
from gpio import GPIO


def line_test():
    line_bot = Line_bot()
    id = 'U44a5e3e3cf9c8835a64bb1273b08f457'
    for i in range(5):
        line_bot.sent_message(id,'gay')
        
def gpio_test():
    print("")
    

if __name__ == "__main__":
    gpio_test()


# 设置判断参数
# 初始化计数器
# 遍历每一帧
# 检测人脸
# 遍历每一个检测到的人脸
# 获取坐标
# 分别计算ear值
# 算一个平均的
# 绘制眼睛区域
# 检查是否满足阈值
# 显示

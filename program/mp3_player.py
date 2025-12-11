import pygame

# 初始化
pygame.mixer.init()

# 載入音檔
pygame.mixer.music.load("C:\\Users\\hp890\\桌面\\hq-天上太阳红彤彤.mp3")  # 這裡換成你的檔案路徑

# 播放
pygame.mixer.music.play()

# 等待播放結束
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
import pygame

# 初始化
pygame.mixer.init()

# 載入音檔
pygame.mixer.music.load("static/alcohol warning.mp3")  # 這裡換成你的檔案路徑

# 播放
pygame.mixer.music.play(loops=3)

# 等待播放結束
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
print("音樂播放結束")
import pygame
import threading
import os
from queue import Queue
from .logs import Log

class MP3Player:
    """mp3音效播放器類別"""
    def __init__(self, static_dir="static"):
        """
        初始化 MP3Player 類別
        
        :param static_dir: 靜態資源目錄，預設為 "static"
        """
        # 初始化 pygame 音效模組
        pygame.mixer.init()
        self.static_dir = static_dir
        # 取得 static 資料夾下所有 mp3 檔案
        self.mp3_files = [f for f in os.listdir(static_dir) if f.endswith(".mp3")]
        self.mp3_paths = {os.path.splitext(f)[0]: os.path.join(static_dir, f) for f in self.mp3_files}
        # 建立播放佇列
        self.queue = Queue()
        self.playing = False
        self.pause_event = threading.Event()
        self.pause_event.set()  # 初始為可播放狀態
        # 啟動播放執行緒
        self.thread = threading.Thread(target=self._play_worker, daemon=True)
        self.thread.start()

    def play(self, name: str, loops=0):
        """
        加入播放請求到佇列
        
        :param name: mp3 檔案名稱（不含副檔名）
        :param loops: 播放次數（預設 1 次）
        """
        if name in self.mp3_paths:
            self.queue.put((self.mp3_paths[name], loops))
            Log.logger.debug(f"已加入播放佇列: {name}")
        else:
            Log.logger.warning(f"找不到音效: {name}")
            
    def next(self):
        """
        播放下一首音效
        """
        pygame.mixer.music.stop()
        Log.logger.debug("已跳至下一首音效")

    def stop_all(self):
        """
        停止所有音效播放
        """
        with self.queue.mutex:
            self.queue.queue.clear()
        pygame.mixer.music.stop()
        Log.logger.debug("已停止所有音效播放")

    def pause(self):
        """
        暫停音效播放（目前播放會繼續，下一首會暫停）
        """
        self.pause_event.clear()
        Log.logger.debug("已暫停音效播放")

    def restart(self):
        """
        恢復音效播放
        """
        self.pause_event.set()
        Log.logger.debug("已恢復音效播放")

    def _play_worker(self):
        """
        執行緒：依序播放佇列中的 mp3
        """
        while True:
            mp3_path, loops = self.queue.get()
            # 檢查是否暫停，若暫停則等待直到恢復
            self.pause_event.wait()
            self.playing = True
            try:
                pygame.mixer.music.load(mp3_path)
                pygame.mixer.music.play(loops=loops)
                # 等待播放結束
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            except Exception as e:
                Log.logger.error(f"播放失敗: {e}")
            self.playing = False
            self.queue.task_done()

    def is_playing(self):
        """
        檢查是否正在播放音效
        
        :return: 若正在播放則返回 True，否則返回 False
        """
        return self.playing
import tkinter as tk
from tkinter import ttk
from alcohol import AlcoholSensor
from face_analyze import FaceAnalyzer
from heart import HeartRateSensor
import threading
import time
from logs import Log


class FatigueMonitorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("疲勞駕駛監控系統")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # 初始化感測器
        self.face_analyzer = FaceAnalyzer()
        self.alcohol_sensor = AlcoholSensor(1)
        self.heart_sensor = HeartRateSensor()

        # 建立UI框架
        self.create_main_frame()
        self.create_status_section()
        self.create_values_section()
        self.create_control_section()
        self.create_log_section()

        # 啟動數據更新線程
        self.running = True
        self.update_thread = threading.Thread(target=self.update_data)
        self.update_thread.daemon = True
        self.update_thread.start()

        # 視窗關閉事件處理
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_main_frame(self):
        """建立主框架"""
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 設定UI樣式
        self.setup_styles()

    def setup_styles(self):
        """設定UI樣式"""
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Status.TLabel', font=('Arial', 10, 'bold'))
        style.configure('Warning.TLabel', foreground='red', font=('Arial', 10, 'bold'))
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TNotebook.Tab', font=('Arial', 10))

    def create_status_section(self):
        """建立狀態顯示區域"""
        status_frame = ttk.LabelFrame(self.main_frame, text="系統狀態", padding="10")
        status_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # 狀態指示灯
        self.status_indicators = {
            "camera": self.create_status_indicator(status_frame, "攝影機", 0),
            "alcohol": self.create_status_indicator(status_frame, "酒精感測", 1),
            "heart": self.create_status_indicator(status_frame, "心率感測", 2),
            "fatigue": self.create_status_indicator(status_frame, "疲勞狀態", 3)
        }

        # 警告標籤
        self.warning_label = ttk.Label(status_frame, text="", foreground="red", style='Warning.TLabel')
        self.warning_label.grid(row=4, column=0, columnspan=2, pady=10)

    def create_status_indicator(self, parent, text, row):
        """建立單個狀態指示灯"""
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, sticky="w", pady=2)

        label = ttk.Label(frame, text=f"{text}:")
        label.pack(side=tk.LEFT)

        canvas = tk.Canvas(frame, width=20, height=20, bg="white", bd=1, relief='solid')
        canvas.pack(side=tk.LEFT, padx=5)

        return canvas

    def create_values_section(self):
        """建立數值顯示區域"""
        values_frame = ttk.LabelFrame(self.main_frame, text="即時數值", padding="10")
        values_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # 數值標籤
        self.value_labels = {
            "alcohol": self.create_value_row(values_frame, "酒精濃度:", "0.000", 0),
            "heart": self.create_value_row(values_frame, "心率:", "0", 1),
            "fatigue": self.create_value_row(values_frame, "疲勞分數:", "0.00", 2),
            "eye": self.create_value_row(values_frame, "眼睛狀態:", "正常", 3),
            "mouth": self.create_value_row(values_frame, "嘴巴狀態:", "正常", 4)
        }

    def create_value_row(self, parent, label_text, default_value, row):
        """建立單個數值顯示行"""
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, sticky="w", pady=2)

        label = ttk.Label(frame, text=label_text)
        label.pack(side=tk.LEFT)

        value_label = ttk.Label(frame, text=default_value, font=('Arial', 10, 'bold'))
        value_label.pack(side=tk.LEFT, padx=5)

        return value_label

    def create_control_section(self):
        """建立控制按鈕區域"""
        control_frame = ttk.LabelFrame(self.main_frame, text="系統控制", padding="10")
        control_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)

        # 控制按鈕
        buttons = [
            ("重置感測器", self.reset_sensors),
            ("測試警告", self.test_warning),
            ("保存日誌", self.save_logs),
            ("退出系統", self.on_close)
        ]

        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(control_frame, text=text, command=command)
            btn.pack(fill=tk.X, pady=5)

    def create_log_section(self):
        """建立日誌顯示區域"""
        log_frame = ttk.LabelFrame(self.main_frame, text="系統日誌", padding="10")
        log_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # 日誌文本框
        self.log_text = tk.Text(log_frame, height=10, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # 滾動條
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)

    def update_data(self):
        """定期更新感測器數據"""
        while self.running:
            try:
                # 更新感測器數據
                self.face_analyzer.update()
                self.alcohol_sensor.update()
                self.heart_sensor.update()

                # 取得最新數據
                alcohol_level = self.alcohol_sensor.get_alcohol()
                heart_rate = self.heart_sensor.get_latest()
                fatigue_score = self.face_analyzer.get_fatigue_score()
                is_fatigued = self.face_analyzer.is_fatigued(fatigue_score)

                # 更新UI
                self.update_ui_values(alcohol_level, heart_rate, fatigue_score, is_fatigued)
                self.update_status_indicators()
                self.check_warnings(alcohol_level, heart_rate, is_fatigued)

            except Exception as e:
                self.log_message(f"更新數據時發生錯誤: {str(e)}")

            time.sleep(0.5)

    def update_ui_values(self, alcohol, heart, fatigue, is_fatigued):
        """更新數值顯示"""
        self.value_labels["alcohol"].config(text=f"{alcohol:.3f}")
        self.value_labels["heart"].config(text=str(heart))
        self.value_labels["fatigue"].config(text=f"{fatigue:.2f}")
        self.value_labels["eye"].config(text="閉眼" if is_fatigued else "正常")
        self.value_labels["mouth"].config(text="張開" if is_fatigued else "正常")

    def update_status_indicators(self):
        """更新狀態指示灯"""
        self.set_indicator_color(self.status_indicators["camera"], "green")
        self.set_indicator_color(self.status_indicators["alcohol"], "green")
        self.set_indicator_color(self.status_indicators["heart"], "green")

        # 疲勞狀態
        fatigue_color = "red" if float(self.value_labels["fatigue"].cget("text")) > 0 else "green"
        self.set_indicator_color(self.status_indicators["fatigue"], fatigue_color)

    def set_indicator_color(self, canvas, color):
        """設定指示灯顏色"""
        canvas.delete("all")
        canvas.create_oval(2, 2, 18, 18, fill=color, outline="black")

    def check_warnings(self, alcohol, heart, is_fatigued):
        """檢查並顯示警告"""
        warnings = []

        if alcohol > 0.15:
            warnings.append("酒精濃度過高!")
        if heart < 60 or heart > 100:
            warnings.append("心率異常!")
        if is_fatigued:
            warnings.append("疲勞警報!")

        if warnings:
            self.warning_label.config(text=" | ".join(warnings), foreground="red")
        else:
            self.warning_label.config(text="系統正常", foreground="green")

    def log_message(self, message):
        """記錄日誌訊息"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)

    def reset_sensors(self):
        """重置所有感測器"""
        self.alcohol_sensor.reset()
        self.log_message("感測器已重置")

    def test_warning(self):
        """測試警告功能"""
        self.warning_label.config(text="測試警告訊息", foreground="red")
        self.log_message("測試警告功能發出")

    def save_logs(self):
        """保存日誌到文件"""
        # 這裡可以添加保存日誌的實際實現
        self.log_message("日誌已保存")

    def on_close(self):
        """處理視窗關閉事件"""
        self.running = False
        self.update_thread.join()
        self.face_analyzer.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FatigueMonitorUI(root)
    root.mainloop()

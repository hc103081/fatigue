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
        self.setup_window()
        self.init_sensors()
        self.create_ui()
        self.start_update_thread()
        self.warning_active = False  # 新增警告狀態 flag


    def setup_window(self):
        """设置窗口基本属性"""
        self.root.title("疲劳驾驶监控系统")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def init_sensors(self):
        """初始化传感器"""
        # 這裡可以根據是否有硬體自動判斷 use_mock
        use_mock = not self.check_hardware_connected()
        self.face_analyzer = FaceAnalyzer()
        self.alcohol_sensor = AlcoholSensor(1, use_mock=use_mock)
        self.heart_sensor = HeartRateSensor(use_mock=use_mock)

    def check_hardware_connected(self):
        # 這裡可以根據實際硬體檢查方式實作
        # 例如嘗試讀取硬體，失敗則回傳 False
        return False  # 預設為測試模式

    def create_ui(self):
        """创建UI界面"""
        self.create_main_frame()
        self.setup_styles()
        self.create_status_section()
        self.create_values_section()
        self.create_control_section()
        self.create_log_section()

    def start_update_thread(self):
        """启动数据更新线程"""
        self.running = True
        self.update_thread = threading.Thread(target=self.update_data)
        self.update_thread.daemon = True
        self.update_thread.start()

    def create_main_frame(self):
        """创建主框架"""
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def setup_styles(self):
        """设置UI样式"""
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Status.TLabel', font=('Arial', 10, 'bold'))
        style.configure('Warning.TLabel', foreground='red', font=('Arial', 10, 'bold'))
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TNotebook.Tab', font=('Arial', 10))

    def create_status_section(self):
        """创建状态显示区域"""
        status_frame = ttk.LabelFrame(self.main_frame, text="系统状态", padding="10")
        status_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # 使用网格布局管理器
        status_frame.grid_columnconfigure(0, weight=1)
        status_frame.grid_rowconfigure(4, weight=1)

        # 状态指示灯
        self.status_indicators = {
            "camera": self.create_status_indicator(status_frame, "攝像頭\t", 0),
            "alcohol": self.create_status_indicator(status_frame, "酒精檢測", 1),
            "heart": self.create_status_indicator(status_frame, "心率檢測", 2),
            "fatigue": self.create_status_indicator(status_frame, "疲劳狀態", 3)
        }

        # 警告标签
        self.warning_label = ttk.Label(status_frame, text="", style='Warning.TLabel')
        self.warning_label.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")

    def create_status_indicator(self, parent, text, row):
        """创建单个状态指示灯"""
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, sticky="w", pady=2)

        label = ttk.Label(frame, text=f"{text}:")
        label.pack(side=tk.LEFT, anchor="center", padx=(0, 5))

        canvas = tk.Canvas(frame, width=20, height=20, bg="white", bd=1, relief='solid')
        canvas.pack(side=tk.LEFT, anchor="center")
        self.set_indicator_color(canvas, "gray")
        return canvas

    def create_values_section(self):
        """创建数值显示区域"""
        values_frame = ttk.LabelFrame(self.main_frame, text="实时数值", padding="10")
        values_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # 使用网格布局管理器
        values_frame.grid_columnconfigure(0, weight=1)

        # 数值标签
        self.value_labels = {
            "alcohol": self.create_value_row(values_frame, "酒精浓度:", "0.000", 0),
            "heart": self.create_value_row(values_frame, "心率:", "0", 1),
            "fatigue": self.create_value_row(values_frame, "疲劳分数:", "0.00", 2),
            "eye": self.create_value_row(values_frame, "眼睛状态:", "正常", 3),
            "mouth": self.create_value_row(values_frame, "嘴巴状态:", "正常", 4)
        }

    def create_value_row(self, parent, label_text, default_value, row):
        """创建单个数值显示行"""
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, sticky="w", pady=2)

        label = ttk.Label(frame, text=label_text)
        label.pack(side=tk.LEFT)

        value_label = ttk.Label(frame, text=default_value, font=('Arial', 10, 'bold'))
        value_label.pack(side=tk.LEFT, padx=5)
        
        return value_label

    def create_control_section(self):
        """创建控制按钮区域"""
        control_frame = ttk.LabelFrame(self.main_frame, text="系统控制", padding="10")
        control_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)
        
        # 使用网格布局管理器
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_rowconfigure(3, weight=1)

        # 控制按钮
        buttons = [
            ("重置传感器", self.reset_sensors),
            ("测试警告", self.test_warning),
            ("保存日志", self.save_logs),
            ("退出系统", self.on_close)
        ]

        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(control_frame, text=text, command=command)
            btn.grid(row=i, column=0, sticky="ew", pady=5)

    def create_log_section(self):
        """创建日志显示区域"""
        log_frame = ttk.LabelFrame(self.main_frame, text="系统日志", padding="10")
        log_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # 使用网格布局管理器
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(0, weight=1)

        # 日志文本框
        self.log_text = tk.Text(log_frame, height=10, state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky="nsew")

        # 滚动条
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text.config(yscrollcommand=scrollbar.set)

    def update_data(self):
        """定期更新传感器数据"""
        while self.running:
            try:
                sensor_data = self.get_sensor_data()
                self.update_ui(sensor_data)
            except Exception as e:
                self.log_message(f"更新数据时发生错误: {str(e)}")
            time.sleep(0.1)

    def get_sensor_data(self):
        """获取传感器数据"""
        face_ok = self.face_analyzer.update()
        self.alcohol_sensor.update()
        self.heart_sensor.update()
    
        return {
            "alcohol_level": self.alcohol_sensor.get_alcohol(),
            "is_alcohol": self.alcohol_sensor.is_over_limit(),
            "heart_rate": self.heart_sensor.get_latest(),
            "is_heart_rate_normal": self.heart_sensor.is_normal(),
            "fatigue_score": self.face_analyzer.get_fatigue_score() if face_ok else 0.0,
            "is_fatigued": self.face_analyzer.is_fatigued() if face_ok else False,
            "camera_ok": face_ok
        }

    def update_ui(self, sensor_data):
        """更新UI界面"""
        self.update_ui_values(
            sensor_data["alcohol_level"],
            sensor_data["heart_rate"],
            sensor_data["fatigue_score"],
            sensor_data["is_fatigued"]
        )
        self.update_status_indicators(sensor_data["camera_ok"])
        
        # 只有在沒有警告時才覆蓋警告文字
        if not self.warning_active:
            self.warning_label.config(text="系统正常", foreground="green")
        self.check_warnings(
            sensor_data["is_alcohol"],
            sensor_data["is_heart_rate_normal"],
            sensor_data["is_fatigued"]
        )

    def update_ui_values(self, alcohol, heart, fatigue, is_fatigued):
        """更新数值显示"""
        self.value_labels["alcohol"].config(text=f"{alcohol:.3f}")
        self.value_labels["heart"].config(text=str(heart))
        self.value_labels["fatigue"].config(text=f"{fatigue:.2f}")
        self.value_labels["eye"].config(text="闭眼" if is_fatigued else "正常")
        self.value_labels["mouth"].config(text="张开" if is_fatigued else "正常")

    def update_status_indicators(self, camera_ok=True):
        """更新状态指示灯"""
        # 攝像頭狀態
        self.set_indicator_color(self.status_indicators["camera"], "green" if camera_ok else "gray")

        # 酒精狀態
        alcohol_color = "yellow" if getattr(self.alcohol_sensor, "is_test_data", False) else "green"
        self.set_indicator_color(self.status_indicators["alcohol"], alcohol_color)

        # 心率狀態
        heart_color = "yellow" if getattr(self.heart_sensor, "is_test_data", False) else "green"
        self.set_indicator_color(self.status_indicators["heart"], heart_color)

        # 疲劳状态
        fatigue_score = float(self.value_labels["fatigue"].cget("text"))
        fatigue_color = "red" if fatigue_score > 0 else "green"
        self.set_indicator_color(self.status_indicators["fatigue"], fatigue_color)
        
    def set_indicator_color(self, canvas, color):
        """设置指示灯颜色"""
        canvas.delete("all")
        canvas.create_oval(2, 2, 18, 18, fill=color, outline="black")

    def check_warnings(self, alcohol, heart, is_fatigued):
        """
        檢查並顯示警告消息
        """
        warnings = []
        if alcohol:
            warnings.append("酒精浓度过高!")
        if heart:
            warnings.append("心率异常!")
        if is_fatigued:
            warnings.append("疲劳警报!")

        warning_text = " | ".join(warnings) if warnings else "系统正常"
        warning_color = "red" if warnings else "green"
        self.warning_label.config(text=warning_text, foreground=warning_color)

    def log_message(self, message):
        """记录日志消息"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)

    def reset_sensors(self):
        """重置所有传感器"""
        self.alcohol_sensor.reset()
        self.log_message("传感器已重置")

    def test_warning(self):
        """测试警告功能"""
        self.warning_active = True
        self.warning_label.config(text="测试警告消息", foreground="red")
        self.log_message("测试警告功能发出")
        self.root.after(2000, self.clear_warning)

    def clear_warning(self):
        """清除警告消息"""
        self.warning_label.config(text="系统正常", foreground="green")
        self.warning_active = False

    def save_logs(self):
        """保存日志到文件"""
        try:
            with open("log/system_log.txt", "w", encoding="utf-8") as log_file:
                log_file.write(self.log_text.get("1.0", tk.END))
            self.log_message("日志已保存")
        except IOError as e:
            self.log_message(f"保存日志时发生IO错误: {str(e)}")
        except Exception as e:
            self.log_message(f"保存日志时发生错误: {str(e)}")



    def on_close(self):
        """处理窗口关闭事件"""
        self.running = False
        if self.update_thread.is_alive():
            self.update_thread.join()
        self.face_analyzer.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FatigueMonitorUI(root)
    root.mainloop()
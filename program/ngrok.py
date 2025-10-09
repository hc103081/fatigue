import subprocess
import shlex
import time
import signal
from logs import Log


def ngrok_start():
    """
    啟動 ngrok 並監看輸出以取得 public url
    """
    # ngrok 可執行檔路徑（Windows 範例）
    NGROK_BIN = r"C:\temp\ngrok-v3-stable-windows-amd64\ngrok.exe"  # 改成路徑
    # Linux / macOS 範例: NGROK_BIN = "/usr/local/bin/ngrok"

    # 構造參數字串
    # 範例：啟動 http 8000，指定 region、name、authtoken 已在 ngrok config
    cmd = f'"{NGROK_BIN}" http --url=undenunciated-ultrared-neil.ngrok-free.app http://127.0.0.1:5000 --log=stdout'

    # 若不希望在命令列顯示 authtoken，可先用 `ngrok authtoken <token>` 做一次設定，之後移除 --authtoken
    proc = subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    Log.logger.debug("ngrok started, PID:", proc.pid)

    # 監看輸出並印出前幾行以取得 public url（ngrok 會在 stdout 輸出啟動資訊）
    
    try:
        time.sleep(1)  # 等待 ngrok 啟動
        for line in proc.stdout:
            Log.logger.debug(line.strip())
            # 可在此以簡單字串解析 public url，例如匹配 "Forwarding
            if "Forwarding" in line and "http" in line:
                Log.logger.debug("可能的 tunnel 行: ", line.strip())
    except KeyboardInterrupt:
        proc.send_signal(signal.SIGINT)
        proc.wait()
        Log.logger.warning("ngrok terminated")
    finally:
        proc.terminate()
        proc.wait()
        Log.logger.debug("ngrok end")

if __name__ == "__main__":
    ngrok_start()
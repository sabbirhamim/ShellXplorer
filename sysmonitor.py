import psutil
import time

class SystemMonitor:
    def run(self, cmd):
        if cmd == "cpu":
            print("CPU Usage:", psutil.cpu_percent(), "%")

        elif cmd == "mem":
            m = psutil.virtual_memory()
            print(f"RAM: {m.percent}% Used")

        elif cmd == "ps":
            for p in psutil.process_iter(['pid','name']):
                print(p.info)

        elif cmd == "top":
            while True:
                print("CPU:", psutil.cpu_percent(), "%", "RAM:", psutil.virtual_memory().percent,"%")
                time.sleep(1)

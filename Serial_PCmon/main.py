import psutil
import serial
import time

# 串口配置
SERIAL_PORT = "COM42"  # Windows
BAUD_RATE = 115200  # 提高波特率，加快数据传输
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

def get_system_stats():
    cpu_samples = []  # 存储 5 次 CPU 采样值

    for _ in range(3):  # 采集 5 次，每次间隔 0.1s
        cpu_samples.append(psutil.cpu_percent(interval=0.05, percpu=False))  # 获取 CPU 使用率
        time.sleep(0.1)  # 间隔 0.1s 采样

    cpu_avg = sum(cpu_samples) / len(cpu_samples)  # 计算 CPU 平均使用率
    cpu_available = cpu_avg  * 10  # 计算 CPU 可用量

    # 读取 RAM 可用比
    ram = psutil.virtual_memory()
    ram_available = (ram.used / ram.total) * 100  # RAM 可用百分比

    return int(cpu_available), int(ram_available), 0, 0  # 先不处理 GPU/VRAM

while True:
    cpu, ram, gpu, vram = get_system_stats()  # 获取数据
    data = f"{cpu},{ram},{gpu},{vram};"  # 格式化数据
    ser.write(data.encode())  # 发送到 ESP32-C3
    print(f"Sent: {data}")  # 调试输出

    time.sleep(0.2)  # 0.5s 发送一次数据

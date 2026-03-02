import os
import time

# 获取当前进程的身份信息
pid = os.getpid()
print(f"警告：正在启动模拟恶意进程！PID（进程身份证号）是: {pid}")
print("这个进程将疯狂占用你的 CPU...")

# 进入无限循环，模拟失控状态
while True:
    # 这一行会让 CPU 进行无意义的计算
    x = 100 * 100
    time.sleep(0.1) # 稍微留一点缝隙，别让你的虚拟机真的死机
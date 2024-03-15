import subprocess
import time
import importlib
import os.path
import sys
from tkinter import Tk, filedialog
from concurrent.futures import ThreadPoolExecutor

# 检查并安装所需的库
libraries = ["subprocess", "time", "importlib", "os.path", "sys", "tkinter", "concurrent.futures"]
for library in libraries:
    try:
        importlib.import_module(library)
    except ModuleNotFoundError:
        print(f"未找到{library}库，正在安装...")
        subprocess.run(["pip", "install", library])
        print(f"{library}库安装完成！")

output_file = f"ip已通_{time.strftime('%Y%m%d%H%M%S')}.csv"
failed_file = f"ip不通_{time.strftime('%Y%m%d%H%M%S')}.csv"

# 清空输出文件
open(output_file, "w").close()
open(failed_file, "w").close()

# 创建Tkinter根窗口
root = Tk()
root.withdraw()  # 隐藏根窗口

# 提示用户选择txt文件
print("这是浪人的小屋折腾的批量ping ip或域名的脚本，谢谢您的支持！请选择您需要ping的txt文件，谢谢")

# 获取文件目录
initial_dir = os.path.dirname(os.path.abspath(__file__))

# 选择输入文件
target_file = filedialog.askopenfilename(title="选择目标地址文件", initialdir=initial_dir, filetypes=[("文本文件", "*.txt")])

# 从文件中读取IP列表
with open(target_file, "r") as f:
    ip_list = f.read().splitlines()

total_ips = len(ip_list)
completed_ips = 0

def ping_ip(ip_or_domain):
    global completed_ips
    completed_ips += 1
    print(f"Pinging {ip_or_domain} [{completed_ips}/{total_ips}]... ", end="")
    sys.stdout.flush()
    
    start_time = time.time()
    result = subprocess.run(["ping", "-n", "1", "-w", "500", ip_or_domain], capture_output=True)
    end_time = time.time()
    
    if result.returncode == 0:
        return f"{ip_or_domain},Success,延迟：{int((end_time - start_time) * 1000)}ms\n"
    else:
        return f"{ip_or_domain},Failed\n"

# 使用线程池进行并行ping操作
with ThreadPoolExecutor() as executor:
    results = executor.map(ping_ip, ip_list)

# 将ping结果写入文件
with open(output_file, "a") as f_output, open(failed_file, "a") as f_failed:
    for result in results:
        if "Success" in result:
            f_output.write(result)
            print("Success")
        else:
            f_failed.write(result)
            print("Failed")

print("Ping")

import psutil
import cpuinfo
import subprocess
import platform

def get_l1_cache():
    try:
        system = platform.system()
        if system == "Windows": #windows
            #using powershell command
            output = subprocess.check_output(["powershell", "-Command",
                                              "(Get-WmiObject Win32_CacheMemory | Where-Object { $_.Level -eq 3 }).MaxCacheSize"],
                                             shell=True, text=True)
            return int(output.strip()) * 1024 if output.strip().isdigit() else None
        elif system == "Linux": #linux
            output = subprocess.check_output("lscpu | grep 'L1d cache'", shell=True, text=True)
            return int(output.split(":")[1].strip().replace("K", "")) * 1024
        elif system == "Darwin":  # macOS
            output = subprocess.check_output("sysctl -n hw.l1dcachesize", shell=True, text=True)
            return int(output.strip())
    except Exception as e:
        print(f"L1 Cache Error: {e}")
        return None

def get_cpu_info():
    info = cpuinfo.get_cpu_info()
    print(f"Processor: {info['brand_raw']}")
    print(f"Architecture: {info['arch']} ({info['bits']}-bit)")
    print(f"Logical Cores (Threads): {psutil.cpu_count(logical=True)}")
    print(f"Physical Cores: {psutil.cpu_count(logical=False)}")

    l1_cache = get_l1_cache()
    if l1_cache:
        print(f"L1 Cache: {l1_cache} bytes")
    if 'l2_cache_size' in info:
        print(f"L2 Cache: {info['l2_cache_size']} bytes")
    if 'l3_cache_size' in info:
        print(f"L3 Cache: {info['l3_cache_size']} bytes")

if __name__ == "__main__":
    get_cpu_info()
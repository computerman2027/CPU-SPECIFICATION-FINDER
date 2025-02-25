import subprocess
import sys
import platform

# Function to install missing packages
def install_package(package, packagename=""):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {packagename}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", packagename])

# Ensure required packages are installed
install_package("psutil", "psutil")
install_package("cpuinfo", "py-cpuinfo")

import psutil
import cpuinfo

def get_l1_cache():
    try:
        system = platform.system()
        if system == "Windows":
            output = subprocess.check_output([
                "powershell", "-Command",
                "(Get-WmiObject Win32_CacheMemory | Where-Object { $_.Level -eq 3 }).MaxCacheSize"
            ], shell=True, text=True)
            return int(output.strip()) * 1024 if output.strip().isdigit() else None
        elif system == "Linux":
            output = subprocess.check_output("lscpu | grep 'L1d cache'", shell=True, text=True)
            return int(output.split(":")[1].strip().replace("K", "")) * 1024
        elif system == "Darwin":
            output = subprocess.check_output("sysctl -n hw.l1dcachesize", shell=True, text=True)
            return int(output.strip())
    except Exception as e:
        print(f"L1 Cache Error: {e}")
        return None

def get_mac_cache_size(level):
    try:
        output = subprocess.check_output(f"sysctl -n hw.l{level}cachesize", shell=True, text=True)
        return int(output.strip())
    except Exception:
        return None

def get_mac_total_cache():
    try:
        output = subprocess.check_output("sysctl -a | grep cachesize", shell=True, text=True)
        cache_info = {}

        for line in output.split("\n"):
            if "hw.perflevel1.l2cachesize" in line:  # L2 cache of P-cores
                cache_info["L2_P"] = int(line.split(":")[1].strip())
            elif "hw.perflevel0.l2cachesize" in line:  # L2 cache of E-cores
                cache_info["L2_E"] = int(line.split(":")[1].strip())
            elif "hw.l3cachesize" in line:  # L3 cache
                cache_info["L3"] = int(line.split(":")[1].strip())

        total_l2 = cache_info.get("L2_P", 0) + cache_info.get("L2_E", 0)
        total_l3 = cache_info.get("L3", 0)

        return total_l2 if total_l2 > 0 else None, total_l3 if total_l3 > 0 else None

    except Exception as e:
        print(f"Error retrieving cache sizes: {e}")
        return None, None

def format_cache_size(size):
    """Convert bytes to human-readable format (KB or MB)"""
    if size is None:
        return "N/A"
    elif size >= 1024 * 1024:
        return f"{size // (1024 * 1024)} MB"
    elif size >= 1024:
        return f"{size // 1024} KB"
    else:
        return f"{size} bytes"

def get_cpu_info():
    info = cpuinfo.get_cpu_info()
    print(f"Processor: {info['brand_raw']}")
    print(f"Architecture: {info['arch']} ({info['bits']}-bit)")
    print(f"Logical Cores (Threads): {psutil.cpu_count(logical=True)}")
    print(f"Physical Cores: {psutil.cpu_count(logical=False)}")

    l1_cache = get_l1_cache()
    print(f"L1 Cache: {format_cache_size(l1_cache)}")

    if platform.system() == "Darwin":
        l2_cache, l3_cache = get_mac_total_cache()
    else:
        l2_cache = get_mac_cache_size(2)
        l3_cache = get_mac_cache_size(3)

    print(f"L2 Cache: {format_cache_size(l2_cache)}")
    print(f"L3 Cache: {format_cache_size(l3_cache)}")

if __name__ == "__main__":
    get_cpu_info()

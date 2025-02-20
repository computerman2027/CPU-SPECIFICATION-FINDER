# CPU Information Script

## Overview
This Python script retrieves and displays detailed CPU information, including:
- Processor name
- Architecture (32-bit/64-bit)
- Number of logical cores (threads)
- Number of physical cores
- L1, L2, and L3 cache sizes

The script is cross-platform and works on **Windows, macOS, and Linux**.

## Requirements
Before running the script, ensure you have the required dependencies installed:

```bash
pip install psutil py-cpuinfo
```

## Usage
Run the script using Python:

```bash
python cpu_features.py
```

## How It Works
- Uses the `psutil` module to get the number of cores and threads.
- Uses `cpuinfo` to fetch detailed CPU specifications.
- Detects the operating system (`Windows`, `Linux`, or `macOS`) and executes the appropriate command to retrieve the L1 cache size:
  - **Windows**: Uses PowerShell to fetch L1 cache size.
  - **Linux**: Extracts cache details using `lscpu`.
  - **macOS**: Uses `sysctl` to get cache size.

## Example Output
```
Processor: AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
Architecture: X86_64 (64-bit)
Logical Cores (Threads): 16
Physical Cores: 8
L1 Cache: 512 KB
L2 Cache: 8388608 bytes
L3 Cache: 16777216 bytes
```

## License
This project is licensed under the MIT License.


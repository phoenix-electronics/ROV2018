import subprocess
from typing import Optional

import psutil


def get_cpu_usage() -> float:
    """Return the current system-wide CPU usage percentage"""
    return psutil.cpu_percent()


def get_cpu_temp() -> Optional[float]:
    """Return the current CPU temperature (if available) in degrees celsius"""
    try:
        temp_str = subprocess.check_output(['sudo', '-n', '/opt/vc/bin/vcgencmd', 'measure_temp'])
        return float(temp_str.replace(b'temp=', b'').replace(b'\'C', b''))
    except (subprocess.CalledProcessError, ValueError):
        pass


def get_mem_usage() -> float:
    """Return the current system-wide memory usage percentage"""
    return psutil.virtual_memory().percent


class SystemInfo:
    """Container for information about the current state of the system"""

    def __init__(self) -> None:
        self.cpu_usage = get_cpu_usage()
        self.cpu_temp = get_cpu_temp()
        self.mem_usage = get_mem_usage()

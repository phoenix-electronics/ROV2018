from subprocess import check_output, CalledProcessError
from typing import Optional

import psutil

from common.message import SystemInfoMessage


def get_cpu_usage() -> float:
    """Return the current system-wide CPU usage percentage"""
    return psutil.cpu_percent()


def get_cpu_temp() -> Optional[float]:
    """Return the current CPU temperature (if available) in degrees celsius"""
    try:
        temp_str = check_output(['sudo', '-n', '/opt/vc/bin/vcgencmd', 'measure_temp'])
        return float(temp_str.replace(b'temp=', b'').replace(b'\'C', b''))
    except (IOError, CalledProcessError, ValueError):
        pass


def get_mem_usage() -> float:
    """Return the current system-wide memory usage percentage"""
    return psutil.virtual_memory().percent


def get_system_info_message() -> SystemInfoMessage:
    """Return a SystemInfoMessage containing information about the current state of the system"""
    return SystemInfoMessage(get_cpu_usage(), get_cpu_temp(), get_mem_usage())

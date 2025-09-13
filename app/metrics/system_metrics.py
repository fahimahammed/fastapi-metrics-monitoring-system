import psutil
import time
import threading
from prometheus_client import Gauge, Counter

from app.config import METRIC_PREFIX

# Metrics
cpu_seconds_total = Counter(f'{METRIC_PREFIX}cpu_seconds_total', 'Total CPU time consumed')
memory_bytes = Gauge(f'{METRIC_PREFIX}resident_memory_bytes', 'Physical memory used')

proc = psutil.Process()

def collect_system_metrics(interval: int):
    while True:
        cpu_seconds_total.inc(proc.cpu_times().user + proc.cpu_times().system)
        memory_bytes.set(proc.memory_info().rss)
        time.sleep(interval)

def start_system_metrics_collector(interval: int):
    thread = threading.Thread(target=collect_system_metrics, args=(interval,), daemon=True)
    thread.start()
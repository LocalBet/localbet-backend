import psutil

class SystemStatsActions:
    def get_stats(self) -> dict:
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        try:
            temps = psutil.sensors_temperatures()
        except Exception:
            temps = None

        return {
            "cpu_percent": cpu,
            "ram_used_mb": mem.used / (1024 * 1024),
            "ram_total_mb": mem.total / (1024 * 1024),
            "disk_used_gb": disk.used / (1024 * 1024 * 1024),
            "disk_total_gb": disk.total / (1024 * 1024 * 1024),
            "temps": temps,
        }

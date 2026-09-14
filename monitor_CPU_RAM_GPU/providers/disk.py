import logging
import re
import subprocess

import psutil

from common.formatting import gb
from common.metrics import DiskMetrics

log = logging.getLogger(__name__)


class DiskProvider:
    def __init__(self) -> None:
        self._temps: dict[str, int] = {}

    def read_all(self) -> list[DiskMetrics]:
        self._temps = self._read_temperatures()
        result: list[DiskMetrics] = []

        for partition in psutil.disk_partitions():
            if not partition.device.startswith("/dev/") or "loop" in partition.device:
                continue
            try:
                usage = psutil.disk_usage(partition.mountpoint)
            except Exception as e:
                log.warning("disk_usage(%s): %s", partition.mountpoint, e)
                continue

            base = partition.device.split("p")[0] if "nvme" in partition.device else partition.device[:-1]
            result.append(DiskMetrics(
                device=partition.device,
                fstype=partition.fstype,
                percent=usage.percent,
                used_gb=gb(usage.used),
                total_gb=gb(usage.total),
                temperature=self._temps.get(base),
            ))
        return result

    @staticmethod
    def _read_temperatures() -> dict[str, int]:
        temps: dict[str, int] = {}
        try:
            out = subprocess.check_output("lsblk -nd -o NAME", shell=True).decode().split()
        except Exception as e:
            log.warning("Не удалось получить список дисков: %s", e)
            return temps

        for name in out:
            if name.startswith("loop"):
                continue
            disk = f"/dev/{name}"
            try:
                if "nvme" in disk:
                    raw = subprocess.check_output(
                        f"sudo nvme smart-log {disk} | grep Temperature", shell=True
                    ).decode()
                    m = re.search(r"Temperature Sensor 1\s*:\s*(\d+)\s*°C", raw)
                    if m:
                        temps[disk] = int(m.group(1))
                elif "sdb" in disk:
                    raw = subprocess.check_output(
                        f"sudo smartctl -A {disk} | grep Temperature", shell=True
                    ).decode()
                    temps[disk] = int(raw.split()[-1])
                else:
                    raw = subprocess.check_output(
                        f"sudo smartctl -A {disk} | grep Temperature", shell=True
                    ).decode()
                    m = re.search(r"(\d+)\s+\(Min/Max", raw)
                    if m:
                        temps[disk] = int(m.group(1))
            except (subprocess.CalledProcessError, ValueError, IndexError):
                pass
        return temps
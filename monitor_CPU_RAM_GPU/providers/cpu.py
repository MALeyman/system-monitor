import logging
import subprocess

import psutil

from common.metrics import CpuMetrics

log = logging.getLogger(__name__)


class CpuProvider:
    def __init__(self) -> None:
        self.cpu_count = psutil.cpu_count(logical=False)
        self.cpu_count_logical = psutil.cpu_count()

    def read(self) -> CpuMetrics:
        return CpuMetrics(
            usage=psutil.cpu_percent(),
            temperature=self._read_temperature(),
            cores=psutil.cpu_percent(percpu=True),
        )

    @staticmethod
    def _read_temperature() -> float | None:
        try:
            output = subprocess.check_output("sensors", shell=True).decode()
        except Exception as e:
            log.warning("Ошибка получения температуры CPU: %s", e)
            return None

        for line in output.splitlines():
            if "Package id" in line or "Tctl" in line:
                try:
                    return float(line.split("+")[1].split("°C")[0].strip())
                except (IndexError, ValueError):
                    return None
        return None
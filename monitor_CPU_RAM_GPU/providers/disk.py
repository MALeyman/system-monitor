import logging
import re
import shutil
import subprocess
import time

import psutil

from common.formatting import gb
from common.metrics import DiskMetrics

log = logging.getLogger(__name__)


def _parse_smartctl_temp(raw: str) -> int | None:
    """Извлекает температуру из вывода smartctl -A.
    Работает для SATA SSD, HDD, NVMe.
    """
    for line in raw.splitlines():
        low = line.lower()
        if "temperature" not in low and "airflow" not in low:
            continue

        # Вариант 1: "30 (Min/Max 15/74)" — берём число ПЕРЕД "(Min/Max"
        m = re.search(r"(\d+)\s*\(Min/Max", line)
        if m:
            return int(m.group(1))

        # Вариант 2: "194 Temperature_Celsius ... 30" — последнее число
        # Но фильтруем — температура обычно 0..120°C
        nums = re.findall(r"\d+", line)
        candidates = [int(n) for n in nums if 0 <= int(n) <= 120]
        if candidates:
            return candidates[-1]

    return None


def _parse_nvme_temp(raw: str) -> int | None:
    """Извлекает температуру из вывода nvme smart-log."""
    # Вариант 1: "temperature : 31 °C"
    m = re.search(r"^temperature\s*:\s*(\d+)", raw, re.MULTILINE | re.IGNORECASE)
    if m:
        return int(m.group(1))
    # Вариант 2: "Temperature Sensor 1 : 45 °C"
    m = re.search(r"Temperature Sensor 1\s*:\s*(\d+)", raw)
    if m:
        return int(m.group(1))
    return None


def _run_privileged(cmd: list[str]) -> str:
    """Запускает команду с sudo -n (без пароля).
    Без pkexec — иначе окно пароля будет появляться каждую секунду.
    Если NOPASSWD не настроен — падает, температура будет N/A.
    """
    return subprocess.check_output(
        ["sudo", "-n"] + cmd,
        stderr=subprocess.DEVNULL,
    ).decode()


class DiskProvider:
    TEMP_INTERVAL = 60  # секунд — как часто обновлять температуры

    def __init__(self) -> None:
        self._temps: dict[str, int] = {}
        self._last_read: float = 0.0

    def read_all(self) -> list[DiskMetrics]:
        # Обновляем температуры не чаще, чем раз в TEMP_INTERVAL секунд
        now = time.time()
        if now - self._last_read >= self.TEMP_INTERVAL:
            self._temps = self._read_temperatures()
            self._last_read = now

        result: list[DiskMetrics] = []
        for partition in psutil.disk_partitions():
            if not partition.device.startswith("/dev/") or "loop" in partition.device:
                continue
            try:
                usage = psutil.disk_usage(partition.mountpoint)
            except Exception as e:
                log.warning("disk_usage(%s): %s", partition.mountpoint, e)
                continue

            # /dev/sdb2 -> /dev/sdb, /dev/nvme0n1p1 -> /dev/nvme0n1
            base = re.sub(r"p?\d+$", "", partition.device)
            result.append(DiskMetrics(
                device=partition.device,
                fstype=partition.fstype,
                percent=usage.percent,
                used_gb=gb(usage.used),
                total_gb=gb(usage.total),
                temperature=self._temps.get(base),
            ))
        return result

    def _read_temperatures(self) -> dict[str, int]:
        temps: dict[str, int] = {}
        try:
            out = subprocess.check_output(
                "lsblk -nd -o NAME", shell=True
            ).decode().split()
        except Exception as e:
            log.warning("Не удалось получить список дисков: %s", e)
            return temps

        for name in out:
            if name.startswith(("loop", "sr", "zram")):
                continue
            disk = f"/dev/{name}"
            temp = None

            try:
                if "nvme" in disk:
                    raw = _run_privileged(["nvme", "smart-log", disk])
                    temp = _parse_nvme_temp(raw)
                else:
                    raw = _run_privileged(["smartctl", "-A", disk])
                    temp = _parse_smartctl_temp(raw)
            except Exception as e:
                log.debug("Не удалось прочитать температуру %s: %s", disk, e)

            if temp is not None:
                temps[disk] = temp
                log.info("Температура %s: %d°C", disk, temp)
            else:
                log.info("Температура %s: N/A", disk)

        return temps

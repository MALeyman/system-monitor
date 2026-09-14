import logging
from typing import Any

from common.formatting import gb
from common.metrics import GpuMetrics

log = logging.getLogger(__name__)

# --- Опциональные зависимости ---------------------------------------------
try:
    import pynvml
    from pynvml import (
        NVMLError_LibraryNotFound,
        nvmlDeviceGetCount,
        nvmlDeviceGetHandleByIndex,
        nvmlDeviceGetMemoryInfo,
        nvmlDeviceGetUtilizationRates,
        nvmlInit,
        nvmlShutdown,
    )
    _HAS_PYNVML = True
except Exception as e:                       # ImportError или любой другой
    _HAS_PYNVML = False
    log.info("pynvml недоступен: %s", e)

try:
    import GPUtil
    _HAS_GPUTIL = True
except Exception as e:
    _HAS_GPUTIL = False
    log.info("GPUtil недоступен: %s", e)


class GpuProvider:
    """Провайдер метрик NVIDIA GPU. Если GPU нет — возвращает пустые метрики."""

    def __init__(self) -> None:
        self.device_count = 0
        self._initialized = False

        if not _HAS_PYNVML:
            log.info("NVIDIA GPU не поддерживается: pynvml не установлен")
            return

        try:
            nvmlInit()
            self.device_count = nvmlDeviceGetCount()
            self._initialized = True
            log.info("NVML инициализирован, устройств: %d", self.device_count)
        except NVMLError_LibraryNotFound:
            log.info("Библиотека NVML не найдена — GPU-метрики недоступны")
        except Exception as e:
            log.warning("Ошибка инициализации NVML: %s", e)

    # ------------------------------------------------------------------
    def available(self) -> bool:
        return self._initialized and self.device_count > 0

    # ------------------------------------------------------------------
    def read(self, index: int = 0) -> GpuMetrics:
        if not self.available():
            return GpuMetrics()

        try:
            handle = nvmlDeviceGetHandleByIndex(index)
            util = nvmlDeviceGetUtilizationRates(handle).gpu
            mem = nvmlDeviceGetMemoryInfo(handle)
            mem_percent = int((mem.used / mem.total) * 100) if mem.total else 0

            name = "GPU"
            temp: float | None = None

            if _HAS_GPUTIL:
                try:
                    gpus = GPUtil.getGPUs()
                    if gpus:
                        name = gpus[index].name if index < len(gpus) else gpus[0].name
                        temp = gpus[index].temperature if index < len(gpus) else gpus[0].temperature
                except Exception as e:
                    log.debug("GPUtil.read: %s", e)

            return GpuMetrics(
                name=name,
                usage=util,
                memory_percent=mem_percent,
                memory_used_gb=gb(mem.used),
                memory_total_gb=gb(mem.total),
                temperature=temp,
            )
        except Exception as e:
            log.warning("Ошибка чтения GPU: %s", e)
            return GpuMetrics()

    # ------------------------------------------------------------------
    def __del__(self) -> None:
        if self._initialized and _HAS_PYNVML:
            try:
                nvmlShutdown()
            except Exception:
                pass
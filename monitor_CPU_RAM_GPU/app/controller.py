import logging

from app.config import REFRESH_MS
from app.router import PAGE_NEEDS
from providers.cpu import CpuProvider
from providers.disk import DiskProvider
from providers.gpu import GpuProvider
from providers.ram import RamProvider

log = logging.getLogger(__name__)


class AppController:
    """Один refresh loop. Собирает метрики и отдаёт их окну."""

    def __init__(self, window):
        self.window = window
        self.cpu = CpuProvider()
        self.ram = RamProvider()
        self.gpu = GpuProvider()
        self.disk = DiskProvider()
        self._job = None
        self._page = 0

    def set_page(self, index: int) -> None:
        self._page = index

    def start(self) -> None:
        self._tick()

    def stop(self) -> None:
        if self._job:
            self.window.after_cancel(self._job)
            self._job = None

    def _tick(self) -> None:
        need = PAGE_NEEDS.get(self._page, {"cpu", "ram"})

        cpu = self.cpu.read() if "cpu" in need else self.cpu.read()  # всё равно нужен для графика
        ram = self.ram.read() if "ram" in need else self.ram.read()
        gpu = self.gpu.read() if "gpu" in need else self.gpu.read()
        disks = self.disk.read_all() if "disk" in need else []

        # на страницах без графиков не обязательно всё читать — но оставим для простоты
        try:
            self.window.render(self._page, cpu, ram, gpu, disks)
        except Exception:
            log.exception("Ошибка обновления окна")

        self._job = self.window.after(REFRESH_MS, self._tick)
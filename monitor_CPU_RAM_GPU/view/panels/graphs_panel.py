from tkinter import ttk

from common.metrics import CpuMetrics, RamMetrics, GpuMetrics
from view.panels.base import BasePanel


class GraphsPanel(BasePanel):
    def __init__(self, master):
        super().__init__(master, "ИСТОРИЯ РЕСУРСОВ")
        self.graphs = None
        self._has_gpu = True   # уточняется в update_data

    def build(self) -> None:
        from view.graphs.graphs_tab import GraphsTab
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=2, pady=5)
        self.graphs = GraphsTab(container)
        super().build()

    def update_data(self, data: tuple[CpuMetrics, RamMetrics, GpuMetrics]) -> None:
        self.ensure_built()
        cpu, ram, gpu = data

        is_available = (gpu.name not in ("N/A", "", None)
                        or gpu.usage > 0
                        or gpu.memory_total_gb > 0)

        if is_available != self._has_gpu:
            self._has_gpu = is_available
            if self.graphs is not None:
                self.graphs.set_gpu_visible(is_available)

        # Обновляем только то, что видно
        if self.graphs is not None:
            self.graphs.update_graphs(
                cpu.usage,
                ram.percent,
                gpu.usage if is_available else 0.0,
            )